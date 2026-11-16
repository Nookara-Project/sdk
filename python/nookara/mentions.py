"""Mentions, channels and message links in Ember message text (Discord's format).

A person is pinged by ``<@id>``, a channel is ``<#cid>``, a role ``<@&rid>`` and a custom emoji ``<:name:eid>``
(``<a:name:eid>`` when animated). A plain ``@name`` or ``#name`` in the text is only text: it pings nobody.

Ids: on Nookara a person's id is their account number (``<@42>``). On an Ember server it is the member's id from that
server, like ``"v:42"`` (a Nookara account), ``"l:3"`` (a local account) or ``"b:7"`` (a bot), so ``<@v:42>``.
Channel ids are the ``cid`` (``"c"`` and 10 hex) everywhere. Bots on the bot API (``/bot/v1``) keep using
Discord's numeric ids; the server turns them into these tokens for you.

    >>> mention("v:42")
    '<@v:42>'
    >>> parse_mentions("hi <@v:42>, see <#c0123456789>")["users"]
    ['v:42']

Links to a channel or a message (``message_link``) show in Ember as a "server > #channel > message" pill.
"""
from __future__ import annotations

import re
from urllib.parse import quote, unquote, urlsplit

EMBER_ORIGIN = 'https://ember.nookara.cc'
USER_TOKEN = re.compile(r'<@!?((?:[vlb]:)?\d{1,20})>')
CHANNEL_TOKEN = re.compile(r'<#(c[0-9a-f]{10})>')
ROLE_TOKEN = re.compile(r'<@&(r[0-9a-f]{10})>')
EMOJI_TOKEN = re.compile(r'<(a?):([A-Za-z0-9_]{1,32}):(e[0-9a-f]{10})>')
_ID = re.compile(r'^(?:[vlb]:)?\d{1,20}$')
_SID = re.compile(r'^s[0-9a-f]{10}$')
_CID = re.compile(r'^c[0-9a-f]{10}$')
_HOME_HOSTS = ('ember.nookara.cc', 'nookara.cc', 'www.nookara.cc', 'velora.ikelene.net')


def _id_of(user):
    if isinstance(user, dict):
        user = user.get('id')
    text = str(user if user is not None else '').strip()
    if not _ID.match(text):
        raise ValueError(f'Not a user id (a number, or v:/l:/b: and a number on an Ember server): {user!r}')
    return text


def _bare(cid):
    if isinstance(cid, dict):
        cid = cid.get('cid')
    return str(cid or '').split('|')[-1].strip()


def mention(user):
    """The text that pings someone: ``<@id>``. Takes the id or a user / member dict with ``id``."""
    return f'<@{_id_of(user)}>'


def channel_mention(channel):
    """The text that links a channel: ``<#cid>``. Takes the cid or a channel dict with ``cid``."""
    cid = _bare(channel)
    if not _CID.match(cid):
        raise ValueError(f'Not a channel id (c and 10 hex): {channel!r}')
    return f'<#{cid}>'


def role_mention(role):
    """The text that pings a role: ``<@&rid>``. Takes the rid or a role dict with ``rid``."""
    rid = str(role.get('rid') if isinstance(role, dict) else role or '').strip()
    if not re.match(r'^r[0-9a-f]{10}$', rid):
        raise ValueError(f'Not a role id (r and 10 hex): {role!r}')
    return f'<@&{rid}>'


def _unique(items):
    out = []
    for x in items:
        if x not in out:
            out.append(x)
    return out


def parse_mentions(text):
    """Everything a message's text points at, in order and without repeats:
    ``{"users": [ids], "channels": [cids], "roles": [rids], "emojis": [{"name", "eid", "animated"}],
    "everyone": bool, "here": bool}``. Only tokens count; a plain ``@name`` is not in ``users``."""
    t = str(text or '')
    emojis, seen = [], set()
    for a, name, eid in EMOJI_TOKEN.findall(t):
        if eid not in seen:
            seen.add(eid)
            emojis.append({'name': name, 'eid': eid, 'animated': a == 'a'})
    return {
        'users': _unique(USER_TOKEN.findall(t)),
        'channels': _unique(CHANNEL_TOKEN.findall(t)),
        'roles': _unique(ROLE_TOKEN.findall(t)),
        'emojis': emojis,
        'everyone': bool(re.search(r'(^|\s)@everyone\b', t)),
        'here': bool(re.search(r'(^|\s)@here\b', t)),
    }


def mentions_user(text, user):
    """Does this text ping that person (a ``<@id>`` token)? Replies and role / @everyone pings aren't counted here."""
    return _id_of(user) in USER_TOKEN.findall(str(text or ''))


def _lookup(table, key, field):
    if callable(table):
        found = table(key)
    else:
        found = (table or {}).get(key)
    if isinstance(found, dict):
        found = found.get('display_name') or found.get(field)
    return found


def plain_text(text, users=None, channels=None, roles=None):
    """Message text with the tokens turned into names, for showing or logging it: ``<@42>`` -> ``@name``,
    ``<#cid>`` -> ``#channel``, ``<@&rid>`` -> ``@role``, ``<:name:eid>`` -> ``:name:``.
    ``users`` / ``channels`` / ``roles`` map an id to a name (or to a dict with ``display_name`` / ``username`` /
    ``name``), or are functions that take the id. Unknown ones come out as ``@unknown-user``, ``#unknown`` and ``@role``."""
    t = str(text or '')
    t = USER_TOKEN.sub(lambda m: f"@{_lookup(users, m.group(1), 'username') or 'unknown-user'}", t)
    t = CHANNEL_TOKEN.sub(lambda m: f"#{_lookup(channels, m.group(1), 'name') or 'unknown'}", t)
    t = ROLE_TOKEN.sub(lambda m: f"@{_lookup(roles, m.group(1), 'name') or 'role'}", t)
    return EMOJI_TOKEN.sub(lambda m: f':{m.group(2)}:', t)


def message_link(sid, cid, message_id=None, *, instance=None, base=EMBER_ORIGIN):
    """A link to a channel, or to one message in it, that Ember opens right there (and shows as a pill when it's
    pasted in a message). ``instance`` is the Ember server's address for a server that lives there."""
    sid, cid = _bare(sid), _bare(cid)
    if not _SID.match(sid) or not _CID.match(cid):
        raise ValueError('sid is s and 10 hex, cid is c and 10 hex')
    at = f'#/i/{quote(str(instance).rstrip("/"), safe="")}' if instance else '#'
    mid = f'/{int(message_id)}' if message_id is not None else ''
    return f'{base.rstrip("/")}/{at}/s/{sid}/{cid}{mid}'


def parse_message_link(url):
    """``{"instance", "sid", "cid", "message_id"}`` for a link to an Ember channel or message (``instance`` is None for
    Nookara's own servers, ``message_id`` None for a channel link), or None when it isn't one."""
    try:
        u = urlsplit(str(url or '').strip())
    except ValueError:
        return None
    if u.scheme not in ('http', 'https') or (u.hostname or '').lower() not in _HOME_HOSTS or u.path not in ('', '/', '/chat', '/chat/'):
        return None
    parts = u.fragment.split('/')
    if not parts or parts[0] != '':
        return None
    parts = parts[1:]
    instance = None
    if parts[:1] == ['i']:
        instance = unquote(parts[1] if len(parts) > 1 else '')
        if not re.match(r'^https?://[^/|]+$', instance):
            return None
        parts = parts[2:]
    if len(parts) < 3 or parts[0] != 's' or not _SID.match(parts[1]) or not _CID.match(parts[2]):
        return None
    mid = parts[3] if len(parts) > 3 and parts[3] else None
    if mid is not None and not re.match(r'^\d{1,20}$', mid):
        return None
    return {'instance': instance, 'sid': parts[1], 'cid': parts[2], 'message_id': mid}
