"""Ember instances: discovery, sessions, community REST, uploads, invites, webhooks, bots, backups and signing.

An instance is a server at its own URL (the main one is https://chat.ikelene.net, Nookara hosts
``e-<slug>.nookara.cc`` servers, and anyone can self-host). It holds one community. Nookara is only
the identity provider: ``login_with_nookara`` asks Nookara for a short token meant for that one instance and
trades it for an instance session. Your Nookara token is never sent to an instance.

Scopes are optional on the consent screen. The ticket carries the instance scopes the person allowed
(``chat``, ``voice``, ``media``, ``sign``); ``Instance.scopes`` lists them and helpers raise
``ScopeError`` when one is missing instead of failing in a confusing way.
"""
from __future__ import annotations

import base64
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

from ._origin import normalize_origin
from .client import APIError, Client, ScopeError, _safe_part
from . import _compat
from .instance_endpoints import InstanceEndpoints
from .scopes import INSTANCE_SCOPES
from .signing import attachment_refs

INSTANCE_OPERATIONS = {r['operationId']: r for r in json.loads(
    Path(__file__).with_name('instance_catalogue.json').read_text(encoding='utf-8'))}

__all__ = ['Instance', 'normalize_origin', 'execute_webhook', 'parse_webhook_url', 'make_alias']


_UNSET = object()


def make_alias(name, avatar_url=None):
    """Build and check an ``alias`` for a bot message: ``{"name", "avatar_url"?}``.

    ``name`` is 1-32 characters and may not contain line breaks (the server also strips zero-width and bidi
    characters). ``avatar_url`` is optional: ``https://`` only, at most 500 characters, no ``user:pass@`` and
    no whitespace; ``None`` or an empty string means no avatar. Only bots may set an alias: a user token is
    answered with ``403 alias_bots_only`` (an ``APIError``). An existing ``{"name", "avatar_url"}`` dict is checked
    and returned as a copy.
    """
    if isinstance(name, dict):
        return make_alias(name.get('name'), name.get('avatar_url'))
    if not isinstance(name, str) or not 1 <= len(name) <= 32 or '\n' in name or '\r' in name:
        raise ValueError('alias name must be 1-32 characters with no line breaks')
    alias = {'name': name}
    if avatar_url:
        if (not isinstance(avatar_url, str) or len(avatar_url) > 500 or not avatar_url.startswith('https://')
                or re.search(r'\s', avatar_url) or '@' in urlsplit(avatar_url).netloc):
            raise ValueError('alias avatar_url must be an https:// URL of at most 500 characters, without spaces or user:pass@')
        alias['avatar_url'] = avatar_url
    return alias


def _alias_field(alias):
    """An ``alias`` argument as a body value: ``None`` clears, a dict or name is checked."""
    return None if alias is None else make_alias(alias)


def parse_webhook_url(url):
    """Split ``https://host/api/v1/webhooks/<id>/<token>`` into (origin, id, token)."""
    p = urlsplit(url)
    m = re.fullmatch(r'/api/v1/webhooks/([^/]+)/([^/]+)', p.path)
    if not m or p.query or p.fragment:
        raise ValueError('Not a Ember webhook URL (expected /api/v1/webhooks/<id>/<token>)')
    return normalize_origin(f'{p.scheme}://{p.netloc}', allow_insecure=p.scheme == 'http'), m[1], m[2]


def execute_webhook(webhook_url, content=None, *, wait=False, username=None, avatar_url=None,
                    embeds=None, files=None, timeout=30, allow_insecure=False, **fields):
    """Post to a webhook URL. No login and no Nookara account needed: the URL is the key."""
    origin, wid, token = parse_webhook_url(webhook_url)
    instance = Instance(origin, timeout=timeout, allow_insecure=allow_insecure)
    return instance.execute_webhook(wid, token, content=content, wait=wait, username=username,
                                    avatar_url=avatar_url, embeds=embeds, files=files, **fields)


DEFAULT_ISSUER = 'https://velora.ikelene.net'
SIG_ISS_ALL = ('https://velora.ikelene.net', 'https://nookara.cc', 'https://ember.nookara.cc')


class Instance(InstanceEndpoints):
    """An instance origin plus (optionally) one instance session or one bot token."""

    def __init__(self, url, session=None, *, bot_token=None, timeout=30, allow_insecure=False,
                 nookara_url='https://nookara.cc', velora_url=None):
        if session and bot_token:
            raise ValueError('Use a session or bot token')
        self.url = normalize_origin(url, allow_insecure=allow_insecure)
        self.allow_insecure = allow_insecure
        nookara_url = _compat.legacy_kwarg('velora_url', velora_url, 'nookara_url', nookara_url, 'https://nookara.cc')
        self.nookara_origin = normalize_origin(nookara_url, allow_insecure=allow_insecure)
        self._http = Client(bot_token or session, base_url=self.url,
                            auth_scheme='Bot' if bot_token else 'Bearer',
                            timeout=timeout, allow_insecure=allow_insecure)
        self.user = None
        self.signer = None
        self.info = None
        self._community = None
        self._scopes = None

    def __repr__(self):
        return f'Instance(url={self.url!r}, authenticated={bool(self._http.token)})'

    @property
    def session(self):
        return self._http.token if self._http.auth_scheme == 'Bearer' else None

    @property
    def bot_token(self):
        return self._http.token if self._http.auth_scheme == 'Bot' else None

    def request(self, method, path, **kwargs):
        """Low-level origin-relative request; never follows redirects."""
        return self._http.request(method, path, **kwargs)

    def call(self, operation_id, *, query=None, json=None, data=None, files=None, raw=False, **params):
        route = INSTANCE_OPERATIONS[operation_id]
        names = {p['name'] for p in route['params']}
        if set(params) != names:
            raise TypeError('Expected path parameters: ' + ', '.join(sorted(names)))
        path = re.sub(r':(\w+)', lambda m: _safe_part(params[m[1]]), route['path'])
        auth = route['auth']
        if auth != 'none' and self._http.auth_scheme != ('Bot' if auth == 'bot' else 'Bearer'):
            raise ValueError('Wrong credential type for this instance route')
        return self.request(route['method'], path, query=query, json=json, data=data,
                            files=files, raw=raw, auth=auth != 'none')

    def discover(self):
        """``/.well-known/bonfire`` (no login): software, protocol, name, ``accounts_mode`` (velora or local),
        ``registration``, ``features``, ``build``, ``max_upload_mb``, ``managed`` (plan on Nookara-hosted servers),
        ``read_only``, ``community`` ({sid, name, member_count, join_policy}) and ``instance_key``."""
        self.info = self.get_well_known_bonfire()
        if not isinstance(self.info, dict) or self.info.get('software') != 'bonfire-server':
            raise ValueError('Not a Ember server (no bonfire-server discovery document)')
        if self.info.get('community'):
            self._community = self.info['community']['sid']
        return self.info

    def _discovered(self):
        return self.info if self.info is not None else self.discover()

    @property
    def accounts_mode(self):
        """``"velora"`` (sign in with a Nookara ticket) or ``"local"`` (username and password)."""
        return self._discovered().get('accounts_mode')

    @property
    def features(self):
        """Discovery ``features``: signing, voice, uploads, youtube, minecraft and bridges."""
        return self._discovered().get('features') or {}

    @property
    def build(self):
        """Discovery ``build``: version, commit, commit_date, built_at, dirty, build_id (None parts when not built by the release script)."""
        return self._discovered().get('build') or {}

    @property
    def read_only(self):
        """True while the instance refuses writes (a hosted server whose paid time ran out)."""
        return bool(self._discovered().get('read_only'))

    def instance_info(self):
        """``GET /api/v1/instance/info``: software, protocol, version, name, build. With an instance admin
        session it also has ``runtime``, ``stats`` and ``update`` (``outdated`` and the ``latest`` official build)."""
        return self.get_api_v1_instance_info()

    def update_available(self):
        """For instance admins: True or False when the instance can tell whether a newer official build exists, else None."""
        update = self.instance_info().get('update')
        return None if not update else bool(update.get('outdated'))

    @property
    def scopes(self):
        """Instance scopes this session holds: a list of ``chat``, ``voice``, ``media``, ``sign``.
        Known right after ``login_with_nookara``; otherwise fetched once from ``/api/v1/me``."""
        if self._scopes is None:
            self._scopes = list((self.me() or {}).get('scopes') or [])
        return list(self._scopes)

    def has_scope(self, name):
        """``instance.has_scope("media")`` (a Nookara identifier such as ``"MEDIA_UPLOAD"`` works too)."""
        name = {v: k for k, v in INSTANCE_SCOPES.items()}.get(name, name)
        return name in self.scopes

    def require_scope(self, name):
        """Raise ``ScopeError`` unless the session holds the instance scope. The person may have declined it
        on the consent screen: ask them to sign in again and keep it ticked."""
        if not self.has_scope(name):
            raise ScopeError(403, {'error': 'insufficient_scope'})

    def _authenticate(self, path, body):
        result = self.request('POST', '/api/v1/auth/' + path, json=body, auth=False)
        token = result['session']
        if not isinstance(token, str) or not token or any(c in token for c in '\r\n'):
            raise ValueError('Invalid instance session response')
        self._http.token, self._http.auth_scheme = token, 'Bearer'
        self.user = result['user']
        return result

    def login_with_nookara(self, nookara=None, *, sign=False, velora_client=None):
        """Sign in with a Nookara account (instances in Nookara-login mode).

        ``nookara`` is a Nookara ``Client`` that holds Chat (2048); without it Nookara answers
        ``ScopeError``. Nookara issues a ticket for this instance only, and just that ticket crosses to the instance.
        ``sign=True`` signs messages automatically and needs Sign Messages (32768) (``ScopeError`` otherwise);
        ``sign="auto"`` signs when the person allowed it and quietly sends unsigned messages when not.
        """
        if velora_client is not None:
            _compat.warn('velora_client=', 'login_with_nookara(nookara)')
            nookara = nookara or velora_client
        if isinstance(nookara, Instance):
            raise TypeError('Pass the Nookara client, not an instance')
        ticket = nookara.post_bonfire_instance_token(json={'instance': self.url})
        result = self._authenticate('velora', {'token': ticket['token']})
        self._scopes = _ticket_scopes(ticket['token'])
        if sign == 'auto':
            if 'sign' in (self._scopes or []):
                self.enable_signing(nookara)
        elif sign:
            self.enable_signing(nookara)
        return result

    def login(self, username, password):
        """Sign in to a local-account instance."""
        return self._authenticate('login', {'username': username, 'password': password})

    def register(self, username, password):
        """Create a local account (instances that allow registration)."""
        return self._authenticate('register', {'username': username, 'password': password})

    def logout(self):
        try:
            return self.post_api_v1_auth_logout()
        finally:
            self._http.token = None
            self.user = None
            self.signer = None
            self._scopes = None

    def me(self):
        """``{user, instance_admin, instance_owner, scopes}`` for this session."""
        return self.get_api_v1_me()

    def enable_signing(self, nookara=None, *, velora_client=None):
        """Fetch the account signing key from Nookara (not the instance) and sign messages from now on."""
        from .signing import Signer
        if velora_client is not None:
            _compat.warn('velora_client=', 'enable_signing(nookara)')
            nookara = nookara or velora_client
        key = nookara.get_bonfire_signing_key()
        self.signer = Signer.from_key_response(key, iss=self.issuer())
        return self.signer

    def issuer(self):
        """The signing issuer this instance announces (``/.well-known/bonfire`` ``velora.issuer``), normalized.
        Falls back to ``https://velora.ikelene.net`` when discovery has none."""
        announced = ((self._discovered() or {}).get('velora') or {}).get('issuer')
        if announced:
            try:
                return normalize_origin(announced, allow_insecure=self.allow_insecure)
            except ValueError:
                pass
        return DEFAULT_ISSUER

    def verify_message(self, message, nookara=None, *, velora=None):
        """Check a signed message yourself (do not trust its ``verified`` flag). Needs ``nookara[signing]``.

        Returns ``(True, "ok")`` or ``(False, reason)``; ``(False, "unsigned")`` for a message without a signature.
        ``nookara`` is a ``Client`` (an anonymous one is made for you); the public key is read from Nookara.
        """
        from .signing import verify_message
        signature = message.get('signature')
        if not signature:
            return False, 'unsigned'
        if velora is not None:
            _compat.warn('velora=', 'verify_message(message, nookara)')
            nookara = nookara or velora
        nookara = nookara or Client(base_url=self.nookara_origin, allow_insecure=self.allow_insecure)
        try:
            key = nookara.get_bonfire_keys_kid_by_kid(kid=signature['kid'])
        except APIError as exc:
            if exc.status == 404:
                return False, 'unknown_key'
            raise
        iss = self.issuer()
        result = verify_message(message, key, iss=iss, instance=self.url)
        if result[0] or result[1] != 'bad_signature':
            return result
        for other in SIG_ISS_ALL:
            if other != iss:
                retry = verify_message(message, key, iss=other, instance=self.url)
                if retry[0]:
                    return retry
        return result

    def community_id(self):
        """The instance has one community; this is its sid (cached)."""
        if self._community is None:
            info = (self.discover() or {}).get('community')
            if info is None:
                raise LookupError('This instance has no community yet')
            self._community = info['sid']
        return self._community

    def _signature(self, sign, cid, body, *, attachments=(), reply_to=None, edit_of=None):
        if sign is False or (sign is None and self.signer is None):
            return None
        if self.signer is None:
            raise ValueError('Signing needs login_with_nookara(client, sign=True) or enable_signing()')
        if not self.user or not self.user.get('velora_id'):
            raise ValueError('Only Nookara accounts can sign messages')
        hashes = attachment_refs(attachments)
        return self.signer.sign(instance=self.url, community=self.community_id(), channel=cid,
                                author=self.user['velora_id'], body=body, attachments=hashes,
                                reply_to=reply_to, edit_of=edit_of)

    def servers(self):
        return self.get_api_v1_servers()['servers']

    def server(self, sid=None):
        return self.get_api_v1_servers_by_sid(sid=sid or self.community_id())

    def community(self):
        return self.server()

    def joined_communities(self):
        """Communities you are a member of on this instance (an instance has one community, so at most one)."""
        return self.servers()

    def create_community(self, name, *, description='', **fields):
        """Set up the community of a fresh instance (instance owner or admin; ``409 community_exists`` otherwise)."""
        return self.post_api_v1_servers(json={'name': name, 'description': description, **fields})

    def update_community(self, sid=None, **fields):
        """PATCH the community: name, description, join_policy (``open`` or ``request``), allow_uploads, upload_max_mb, listed..."""
        return self.patch_api_v1_servers_by_sid(sid=sid or self.community_id(), json=fields)

    def channels(self):
        return self.server()['channels']

    def channel_id(self, name):
        """Channel id for a name like ``general`` or ``#general`` (a cid passes through)."""
        wanted = name.lstrip('#').lower()
        for channel in self.channels():
            if channel.get('name', '').lower() == wanted or channel.get('cid') == name:
                return channel['cid']
        raise LookupError('No channel named ' + name)

    def members(self, sid=None):
        return self.get_api_v1_servers_by_sid_members(sid=sid or self.community_id())

    def join(self, sid=None):
        return self.post_api_v1_servers_by_sid_join(sid=sid or self.community_id())

    def join_invite(self, code):
        """Join through an invite code. An invite always admits you, even when the community asks for approval."""
        return self.post_api_v1_join_by_code(code=code)

    def invite_info(self, code):
        """Public preview of an invite (no login): community name, icon and member count."""
        return self.get_api_v1_invite_by_code(code=code)

    def invites(self, sid=None):
        """Invites of the community (Manage server): ``[{code, created_by, created_at, expires_at, max_uses, uses}]``."""
        return self.get_api_v1_servers_by_sid_invites(sid=sid or self.community_id())['invites']

    def delete_invite(self, code):
        return self.delete_api_v1_invites_by_code(code=code)

    def join_requests(self, sid=None):
        """Pending requests when ``join_policy`` is ``request`` (Kick or Manage server)."""
        return self.get_api_v1_servers_by_sid_requests(sid=sid or self.community_id())['requests']

    def accept_join_request(self, uid, sid=None):
        return self.post_api_v1_servers_by_sid_requests_by_uid_accept(sid=sid or self.community_id(), uid=uid)

    def deny_join_request(self, uid, sid=None):
        return self.post_api_v1_servers_by_sid_requests_by_uid_deny(sid=sid or self.community_id(), uid=uid)

    def leave(self, sid=None):
        return self.post_api_v1_servers_by_sid_leave(sid=sid or self.community_id())

    def create_invite(self, sid=None, *, expires_in=None, max_uses=None, **options):
        """Make an invite (Manage server). ``expires_in`` is seconds, ``max_uses`` a count; both optional."""
        body = {k: v for k, v in {'expires_in': expires_in, 'max_uses': max_uses, **options}.items() if v is not None}
        return self.post_api_v1_servers_by_sid_invites(sid=sid or self.community_id(), json=body)

    def create_channel(self, name, *, type='text', category=None, topic=None, config=None, sid=None):
        """Types: text, voice, logs, roles, welcome, link, starboard, game. ``config`` depends on the type."""
        body = {k: v for k, v in {'name': name, 'type': type, 'category': category, 'topic': topic, 'config': config}.items() if v is not None}
        return self.post_api_v1_servers_by_sid_channels(sid=sid or self.community_id(), json=body)

    def update_channel(self, cid, **fields):
        return self.patch_api_v1_channels_by_cid(cid=cid, json=fields)

    def delete_channel(self, cid):
        return self.delete_api_v1_channels_by_cid(cid=cid)

    def set_channel_permissions(self, cid, overwrites):
        """Replace the role overwrites: ``[{"rid": ..., "allow": 1024, "deny": 0}]`` (View 1024, Send 1, Attach 256)."""
        return self.put_api_v1_channels_by_cid_perms(cid=cid, json={'overwrites': overwrites})

    def kick(self, uid, *, ban=False, sid=None):
        """Remove a member by principal id (``v:123``); ``ban=True`` also bans them."""
        return self.delete_api_v1_servers_by_sid_members_by_uid(sid=sid or self.community_id(), uid=uid, query={'ban': 1} if ban else None)

    def bans(self, sid=None):
        return self.get_api_v1_servers_by_sid_bans(sid=sid or self.community_id())

    def unban(self, uid, sid=None):
        return self.delete_api_v1_servers_by_sid_bans_by_uid(sid=sid or self.community_id(), uid=uid)

    def remove_role(self, uid, rid, *, sid=None):
        return self.delete_api_v1_servers_by_sid_members_by_uid_roles_by_rid(sid=sid or self.community_id(), uid=uid, rid=rid)

    def identities(self, ids):
        """Resolve principal ids (``v:12``, ``l:3``, ``b:1``) to user objects, for example after a reconnect."""
        return self.get_api_v1_identities(query={'ids': ','.join(ids)})['users']

    def user_settings(self):
        """Your per-instance settings (``GET /api/v1/settings``), for example ``server_order``."""
        return self.get_api_v1_settings()

    def update_user_settings(self, **changes):
        return self.patch_api_v1_settings(json=changes)

    def notify_levels(self):
        return self.get_api_v1_notify()

    def set_notify(self, target, *, level='default', mute_minutes=0, push=True):
        """Notification level for a community or channel: default, all, mentions or none. ``mute_minutes`` 0 unmutes, -1 mutes for good."""
        return self.put_api_v1_notify_by_target(target=target, json={'level': level, 'mute_minutes': mute_minutes, 'push': push})

    def emojis(self, sid=None):
        return self.get_api_v1_servers_by_sid_emojis(sid=sid or self.community_id())

    def create_role(self, name, *, sid=None, **fields):
        return self.post_api_v1_servers_by_sid_roles(sid=sid or self.community_id(), json={'name': name, **fields})

    def assign_role(self, uid, rid, *, sid=None):
        return self.put_api_v1_servers_by_sid_members_by_uid_roles_by_rid(sid=sid or self.community_id(), uid=uid, rid=rid)

    def messages(self, cid, *, before=None, after=None, limit=50):
        return self.get_api_v1_channels_by_cid_messages(cid=cid, query=dict(before=before, after=after, limit=limit))

    def send_message(self, cid, message, *, reply_to=None, attachments=None, signature=None, sign=None, alias=None):
        """Post a message. ``sign=None`` signs when signing is enabled; ``False`` never signs.

        ``alias={"name": ..., "avatar_url": ...}`` (or ``make_alias(...)``) is for bot tokens only."""
        if signature is None:
            signature = self._signature(sign, cid, message, attachments=attachments or (), reply_to=reply_to)
        body = dict(message=message, reply_to=reply_to, attachments=attachments or [])
        if signature is not None:
            body['signature'] = signature
        if alias is not None:
            body['alias'] = make_alias(alias)
        return self.post_api_v1_channels_by_cid_messages(cid=cid, json=body)

    def edit_message(self, message_id, message, *, channel=None, sign=None, alias=_UNSET):
        """Edit a message. Bots can pass ``alias=`` to change it or ``alias=None`` to clear it."""
        body = {'message': message}
        if alias is not _UNSET:
            body['alias'] = _alias_field(alias)
        if sign is not False and self.signer is not None:
            if channel is None:
                raise ValueError('Pass channel=<cid> to sign an edit')
            body['signature'] = self._signature(sign, channel, message, edit_of=message_id)
        return self.patch_api_v1_messages_by_id(id=message_id, json=body)

    def delete_message(self, message_id):
        return self.delete_api_v1_messages_by_id(id=message_id)

    def react(self, message_id, emoji):
        return self.put_api_v1_messages_by_id_reactions_by_emoji(id=message_id, emoji=emoji)

    def unreact(self, message_id, emoji):
        return self.delete_api_v1_messages_by_id_reactions_by_emoji(id=message_id, emoji=emoji)

    def pin(self, message_id):
        return self.put_api_v1_messages_by_id_pin(id=message_id)

    def unpin(self, message_id):
        return self.delete_api_v1_messages_by_id_pin(id=message_id)

    def pins(self, cid):
        return self.get_api_v1_channels_by_cid_pins(cid=cid)

    def search(self, cid, query):
        return self.get_api_v1_channels_by_cid_search(cid=cid, query={'q': query})

    def upload(self, file, *, sid=None, cid=None):
        """Upload a file (path or ``(name, bytes, mime)``) to the community. Needs the ``media`` scope (Upload Media)
        and the community's ``allow_uploads``; ``ScopeError`` if the person declined it. Pass ``cid`` to have the
        channel's Attach permission checked up front.

        Returns ``{url, name, size, mime, type, sha256, ...}``; pass it in ``attachments=[...]``.
        """
        self._need('media')
        return self.post_api_v1_media_upload(query={'sid': sid or self.community_id(), 'cid': cid}, files={'file': file})

    def import_media(self, url, *, name=None, sid=None, cid=None):
        """Have the instance fetch an https URL and store it as an upload (same checks and response as ``upload``).
        Use it for saved files hosted elsewhere, then attach the result; the instance hashes the stored bytes."""
        self._need('media')
        body = {'url': url, **({'name': name} if name else {})}
        return self.post_api_v1_media_import(query={'sid': sid or self.community_id(), 'cid': cid}, json=body)

    def _need(self, scope):
        """Fail early and clearly when a session is known to lack an instance scope."""
        if self._scopes is not None and scope not in self._scopes:
            raise ScopeError(403, {'error': 'insufficient_scope'})

    def mark_read(self, cid, message_id):
        return self.post_api_v1_channels_by_cid_read(cid=cid, json={'message_id': message_id})

    def webhooks(self, cid):
        return self.get_api_v1_channels_by_cid_webhooks(cid=cid)['webhooks']

    def create_webhook(self, cid, name):
        return self.post_api_v1_channels_by_cid_webhooks(cid=cid, json={'name': name})

    def update_webhook(self, wid, **fields):
        """name, avatar, channel (move it) or ``new_token=True`` to rotate the secret."""
        return self.patch_api_v1_hooks_by_wid(wid=wid, json=fields)

    def delete_webhook(self, wid):
        return self.delete_api_v1_hooks_by_wid(wid=wid)

    def execute_webhook(self, wid, token, content=None, *, wait=False, files=None, username=None,
                        avatar_url=None, embeds=None, **fields):
        """Post through a webhook. Works on an Instance with no login at all."""
        payload = {k: v for k, v in {**fields, 'content': content, 'username': username,
                                     'avatar_url': avatar_url, 'embeds': embeds}.items() if v is not None}
        args = dict(query={'wait': wait})
        if files is None:
            args['json'] = payload
        else:
            args.update(data={'payload_json': json.dumps(payload, ensure_ascii=False)}, files=files)
        return self.post_api_v1_webhooks_by_wid_by_token(wid=wid, token=token, **args)

    def bots(self):
        return self.get_api_v1_bots()

    def create_bot(self, name, description=''):
        """Returns ``{bot, token}``. The token is shown once; keep it secret."""
        return self.post_api_v1_bots(json={'name': name, 'description': description})

    def update_bot(self, bot_id, **fields):
        """name, description (a bot from the Nookara gallery is managed by Nookara: ``403 gallery_bot_managed``)."""
        return self.patch_api_v1_bots_by_id(id=bot_id, json=fields)

    def delete_bot(self, bot_id):
        return self.delete_api_v1_bots_by_id(id=bot_id)

    def bot_by_name(self, username):
        return self.get_api_v1_bots_by_name_by_username(username=username)

    def reset_bot_token(self, bot_id):
        return self.post_api_v1_bots_by_id_token(id=bot_id)

    def add_bot(self, username, sid=None):
        return self.post_api_v1_bots_by_name_by_username_add(username=username, json={'sid': sid or self.community_id()})

    def add_gallery_bot(self, ticket, sid=None):
        """Add a bot from the Nookara bot gallery to the community with a ticket from ``Client.gallery_ticket``."""
        return self.post_api_v1_bots_gallery_add(json={'ticket': ticket, 'sid': sid or self.community_id()})

    def bot_send(self, channel_id, content, *, alias=None, **fields):
        """With a bot token: post to a channel (numeric channel id from the bot REST API).

        ``alias={"name": "Narrator", "avatar_url": "https://..."}`` shows the message under another name and
        avatar; the author stays this bot. See ``make_alias`` for the limits."""
        body = {'content': content, **fields}
        if alias is not None:
            body['alias'] = make_alias(alias)
        return self.post_bot_v1_channels_by_cid_messages(cid=channel_id, json=body)

    def bot_discovery(self):
        """``GET /bot/discovery`` (no token): the REST and gateway addresses of this instance."""
        return self.get_bot_discovery()

    def bot_me(self):
        return self.get_bot_v1_users_me()

    def bot_guilds(self):
        return self.get_bot_v1_users_me_guilds()

    def bot_channels(self, guild_id):
        return self.get_bot_v1_guilds_by_gid_channels(gid=guild_id)

    def bot_members(self, guild_id):
        return self.get_bot_v1_guilds_by_gid_members(gid=guild_id)

    def bot_messages(self, channel_id, *, limit=50, before=None, after=None):
        return self.get_bot_v1_channels_by_cid_messages(cid=channel_id, query={'limit': limit, 'before': before, 'after': after})

    def bot_edit(self, channel_id, message_id, content=None, *, alias=_UNSET):
        """Edit the bot's own message. ``alias=`` changes the alias, ``alias=None`` clears it; leave it out to keep it."""
        body = {}
        if content is not None:
            body['content'] = content
        if alias is not _UNSET:
            body['alias'] = _alias_field(alias)
        if not body:
            raise ValueError('Pass content and/or alias')
        return self.patch_bot_v1_channels_by_cid_messages_by_mid(cid=channel_id, mid=message_id, json=body)

    def bot_delete(self, channel_id, message_id):
        return self.delete_bot_v1_channels_by_cid_messages_by_mid(cid=channel_id, mid=message_id)

    def bot_react(self, channel_id, message_id, emoji):
        return self.put_bot_v1_channels_by_cid_messages_by_mid_reactions_by_emoji_me(cid=channel_id, mid=message_id, emoji=emoji)

    def backups(self):
        return self.get_api_v1_instance_backups()['backups']

    def create_backup(self, note=None):
        return self.post_api_v1_instance_backups(json={'note': note} if note else {})['backup']

    def download_backup(self, backup_id):
        return self.get_api_v1_instance_backups_by_id_download(id=backup_id, raw=True)

    def delete_backup(self, backup_id):
        return self.delete_api_v1_instance_backups_by_id(id=backup_id)

    def restore_backup(self, backup_id):
        return self.post_api_v1_instance_backups_by_id_restore(id=backup_id)

    def restore_from_file(self, path):
        return self.post_api_v1_instance_restore(files={'file': path})

    def settings(self):
        return self.get_api_v1_instance_settings()

    def update_settings(self, **changes):
        return self.patch_api_v1_instance_settings(json=changes)

    def restart(self):
        return self.post_api_v1_instance_restart()

    def claim(self, code):
        """Claim a fresh instance with the setup code printed on first boot (you become owner and admin)."""
        return self.post_api_v1_instance_claim(json={'code': code})

    def admins(self):
        return self.get_api_v1_instance_admins()

    def add_admin(self, uid):
        return self.put_api_v1_instance_admins_by_uid(uid=uid)

    def remove_admin(self, uid):
        return self.delete_api_v1_instance_admins_by_uid(uid=uid)

    def register_with_nookara(self):
        """Register now with Nookara (push, payments, daily credits, voice broker, directory). Admins only."""
        return self.post_api_v1_instance_velora_register()

    def owner_attestation(self):
        """Owner only: proof for ``Client.post_bonfire_instances_payout`` so role-shop credits reach the owner's account."""
        return self.get_api_v1_instance_owner_attestation()

    def export_community(self, sid=None):
        """The community as a ``bonfire-export-v1`` zip (bytes). Owner only."""
        return self.get_api_v1_servers_by_sid_export(sid=sid or self.community_id(), raw=True)

    def import_community(self, path):
        """Create the community from an export zip (only while the instance has no community)."""
        return self.post_api_v1_import(files={'file': path})

    def import_from_nookara(self, ticket):
        """Create the community from a Discord / Fluxer bundle prepared with ``Client.start_ember_import``."""
        return self.post_api_v1_import_velora(json={'ticket': ticket})

    def game_connected(self, *, q=None, tag=None, page=None):
        """Game servers that connected with ``ember server <this url>`` and wait to be linked (Manage server)."""
        return self.get_api_v1_game_connected(query={'q': q, 'tag': tag, 'page': page})

    def game_link(self, iid, *, cid=None):
        """Link a connected game server, optionally to a game channel that has no server yet."""
        return self.post_api_v1_game_connected_by_iid_link(iid=iid, json={'cid': cid} if cid else {})

    def game_claim(self, cid=None, *, hint=None):
        """Alternative: a code to run as ``ember link CODE`` in the game server's console."""
        body = {k: v for k, v in {'cid': cid, 'hint': hint}.items() if v}
        return self.post_api_v1_game_claims(json=body)

    def game_linked(self, sid=None):
        return self.get_api_v1_game_servers_by_sid_instances(sid=sid or self.community_id())['instances']

    def game_status(self, cid):
        return self.get_api_v1_game_channels_by_cid_status(cid=cid)

    def game_exec(self, cid, command):
        """Run a console command (Manage server; the Ember apps and the website may be required by the server)."""
        return self.post_api_v1_game_channels_by_cid_console(cid=cid, json={'command': command})

    def bridge_platforms(self):
        return self.get_api_v1_bridge_platforms()['platforms']

    def cloudlink_status(self, cid):
        return self.get_api_v1_channels_by_cid_cloudlink(cid=cid)['status']

    def gateway(self, **kwargs):
        """User gateway for an instance session. Use ``async with``."""
        from .instance_gateway import InstanceGateway
        if not self.session:
            raise ValueError('Gateway requires an instance session')
        return InstanceGateway(self, **kwargs)

    def bot_gateway(self, **kwargs):
        """Discord-style bot gateway for an instance with a bot token."""
        from .instance_gateway import BotGateway
        if not self.bot_token:
            raise ValueError('Bot gateway requires a bot token')
        return BotGateway(self, **kwargs)


def _ticket_scopes(token):
    """The ``scp`` claim of the instance ticket we just traded (read, not verified: the instance verified it)."""
    try:
        claims = json.loads(base64.urlsafe_b64decode(token.split('.')[1] + '=' * (-len(token.split('.')[1]) % 4)))
        scp = claims.get('scp')
        return [s for s in scp if s in INSTANCE_SCOPES] if isinstance(scp, list) else None
    except (IndexError, ValueError, TypeError):
        return None


_compat.add_aliases(Instance, {'login_with_velora': 'login_with_nookara', 'register_with_velora': 'register_with_nookara',
                               'import_from_velora': 'import_from_nookara'})
Instance.velora_origin = _compat.renamed_attribute('Instance.velora_origin', 'nookara_origin')
