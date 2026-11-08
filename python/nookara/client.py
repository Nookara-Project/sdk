from __future__ import annotations

import json as _json
import mimetypes
import re
import time
import uuid
import warnings
import webbrowser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from ._origin import normalize_origin
from ._version import __version__
from .endpoints import Endpoints
from .scopes import SCOPE_LABELS, has_scope as _has_scope, scope_bit, scope_names as _scope_names

BASE_URL = "https://nookara.cc"
CATALOGUE = _json.loads(Path(__file__).with_name("catalogue.json").read_text(encoding="utf-8"))
OPERATIONS = {r["operationId"]: r for r in CATALOGUE["routes"]}
SCOPES = CATALOGUE["scopes"]
MAX_MULTIPART_BYTES = 64 * 1024 * 1024


class APIError(Exception):
    """HTTP or protocol error. Inspect status, error, payload and retry_after."""

    def __init__(self, status, payload, headers=None):
        self.status = status
        self.payload = payload
        self.error = payload.get("error", payload.get("message", "api_error")) if isinstance(payload, dict) else "http_error"
        self.required_scope = payload.get("required_scope") if isinstance(payload, dict) else None
        self.disabled_by_admin = bool(payload.get("disabled_by_admin")) if isinstance(payload, dict) else False
        self.moved_to = payload.get("moved_to") if isinstance(payload, dict) else None
        self.reason = payload.get("reason") if isinstance(payload, dict) else None
        value = (headers or {}).get("Retry-After")
        if isinstance(payload, dict):
            value = payload.get("retry_after", value)
        try:
            self.retry_after = max(0.0, float(value)) if value is not None else None
        except (ValueError, TypeError):
            self.retry_after = None
        safe = str(self.error)
        label = safe if re.fullmatch(r"[a-zA-Z0-9_ :.-]{1,100}", safe) else "api_error"
        super().__init__(f"Nookara API {status}: {label}")


class ScopeError(APIError):
    """A token lacks a scope for this call (``insufficient_scope``) or an admin switched the service off
    for the account (``scope_disabled``). Scopes are optional on the consent screen, so a person may have
    declined it: show a "log in again to use this" message instead of failing hard.

    ``scope`` is the identifier (for example ``"MEDIA_UPLOAD"``) when the server named the scope bit,
    ``label`` its consent-screen name, ``disabled_by_admin`` is true for ``scope_disabled``.
    Instances answer a plain ``insufficient_scope`` without a bit.
    """

    def __init__(self, status, payload, headers=None):
        super().__init__(status, payload, headers)
        bit = self.required_scope
        self.scope = next((n for n, b in SCOPES.items() if b == bit), None) if isinstance(bit, int) else None
        self.label = SCOPE_LABELS.get(self.scope) if self.scope else None


class TransportError(Exception):
    """Network failure. A failed write may already have reached the server."""


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _safe_part(value):
    value = str(value)
    if not value or value in (".", ".."):
        raise ValueError("Path parameters cannot be empty or dot segments")
    return quote(value, safe="")


def _multipart(data, files):
    boundary = "velora-" + uuid.uuid4().hex
    chunks = []
    total = 0
    def quoted(value):
        value = str(value)
        if any(c in value for c in '\r\n"\\'):
            raise ValueError("Invalid multipart field or filename")
        return value
    for name, value in (data or {}).items():
        if value is None:
            continue
        if isinstance(value, (dict, list, bool)):
            value = _json.dumps(value, ensure_ascii=False)
        chunks.extend([f'--{boundary}\r\nContent-Disposition: form-data; name="{quoted(name)}"\r\n\r\n'.encode(), str(value).encode("utf-8"), b"\r\n"])
    for name, value in files.items():
        if isinstance(value, (str, Path)):
            p = Path(value)
            if p.stat().st_size > MAX_MULTIPART_BYTES:
                raise ValueError("Upload too large for buffered multipart; use chunked video upload")
            filename, content = p.name, p.read_bytes()
            mime = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        else:
            filename, content, mime = value
            if hasattr(content, "read"):
                content = content.read(MAX_MULTIPART_BYTES + 1)
            content = bytes(content)
        total += len(content)
        if total > MAX_MULTIPART_BYTES:
            raise ValueError("Uploads exceed the SDK's 64 MiB buffered limit; use chunks")
        if "\r" in mime or "\n" in mime:
            raise ValueError("Invalid MIME type")
        chunks.extend([f'--{boundary}\r\nContent-Disposition: form-data; name="{quoted(name)}"; filename="{quoted(filename)}"\r\nContent-Type: {mime}\r\n\r\n'.encode("utf-8"), content, b"\r\n"])
    chunks.append(f"--{boundary}--\r\n".encode())
    return b"".join(chunks), "multipart/form-data; boundary=" + boundary


class Client(Endpoints):
    """Synchronous REST client. No automatic retries of reads or writes."""

    def __init__(self, token=None, *, base_url=BASE_URL, auth_scheme="Bearer", timeout=30, allow_insecure=False, origin=None):
        parsed = urlsplit(base_url)
        if parsed.scheme not in ("https", "http") or not parsed.netloc or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ValueError("base_url must be an HTTP(S) origin without credentials or query")
        if parsed.scheme != "https" and not allow_insecure:
            raise ValueError("HTTPS required; allow_insecure is for local tests only")
        if auth_scheme not in ("Bearer", "Bot"):
            raise ValueError("auth_scheme must be Bearer or Bot")
        if token and any(c in token for c in "\r\n"):
            raise ValueError("Invalid token")
        self.token, self.base_url = token, base_url.rstrip("/")
        self.origin = origin
        self.auth_scheme, self.timeout = auth_scheme, timeout
        self._opener = build_opener(_NoRedirect())

    def __repr__(self):
        return f"Client(base_url={self.base_url!r}, authenticated={bool(self.token)})"

    def request(self, method, path, *, query=None, json=None, data=None, files=None, auth=True, raw=False):
        """Call a relative route. JSON/text is decoded; raw=True returns bytes."""
        if not path.startswith("/") or path.startswith("//") or "\\" in path or "#" in path:
            raise ValueError("Use an origin-relative API path")
        if json is not None and (data is not None or files is not None):
            raise ValueError("Use json OR multipart/form fields")
        params = {}
        for key, value in (query or {}).items():
            if value is not None:
                params[key] = str(value).lower() if isinstance(value, bool) else value
        url = self.base_url + path
        if params:
            url += ("&" if "?" in path else "?") + urlencode(params, doseq=True)
        headers = {"Accept": "application/json", "User-Agent": "nookara-python/" + __version__}
        if auth and self.token:
            headers["Authorization"] = self.auth_scheme + " " + self.token
        if self.origin:
            headers["Origin"] = self.origin
        body = None
        if json is not None:
            body = _json.dumps(json, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"
        elif files is not None:
            body, headers["Content-Type"] = _multipart(data, files)
        elif data is not None:
            body = urlencode(data).encode()
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        req = Request(url, data=body, headers=headers, method=method.upper())
        try:
            with self._opener.open(req, timeout=self.timeout) as response:
                content = response.read()
                content_type = response.headers.get("Content-Type", "")
        except HTTPError as exc:
            content = exc.read()
            exc.close()
            try:
                payload = _json.loads(content)
            except (ValueError, UnicodeDecodeError):
                payload = {"error": "http_error"}
            if exc.code == 403 and isinstance(payload, dict) and payload.get("error") in ("insufficient_scope", "scope_disabled"):
                raise ScopeError(exc.code, payload, exc.headers) from None
            raise APIError(exc.code, payload, exc.headers) from None
        except (URLError, TimeoutError, OSError):
            raise TransportError("Nookara request failed; check connectivity before retrying writes") from None
        if raw:
            return content
        if not content:
            return None
        if "json" in content_type:
            return _json.loads(content)
        if content_type.startswith("text/"):
            return content.decode("utf-8")
        return content

    def call(self, operation_id, *, query=None, json=None, data=None, files=None, raw=False, **path_params):
        route = OPERATIONS[operation_id]
        names = {p["name"] for p in route["params"]}
        if set(path_params) - names:
            raise TypeError("Unknown path parameters: " + ", ".join(sorted(set(path_params) - names)))
        path = route["path"]
        for param in route["params"]:
            name = param["name"]
            value = path_params.get(name)
            if value is None:
                if not param["optional"]:
                    raise TypeError("Missing path parameter: " + name)
                path = path.replace("/:" + name + "?", "")
            else:
                path = path.replace(":" + name + ("?" if param["optional"] else ""), _safe_part(value))
        auth = route["auth"]
        if self.token and auth in ("bearer", "bot") and self.auth_scheme != ("Bot" if auth == "bot" else "Bearer"):
            raise ValueError("This route requires " + auth + " authentication")
        return self.request(route["method"], path, query=query, json=json, data=data, files=files, raw=raw, auth=auth in ("bearer", "bot"))

    def product(self, product_id):
        """A product's public details: name, price, plans, who gets the money, the managing app."""
        return self.request("GET", f"/products/{quote(str(product_id), safe='')}")["product"]

    def products_of(self, username):
        """What someone sells."""
        return self.request("GET", "/products", query={"seller": username})["products"]

    def add_to_cart(self, product_id, *, plan=None, quantity=None):
        """Put a product in the cart (no credits scope needed). plan: "period" or "yearly". Returns ``checkout_url``: open it for the person."""
        body = {"product_id": product_id}
        if plan is not None:
            body["plan"] = plan
        if quantity is not None:
            body["quantity"] = quantity
        return self.request("POST", "/cart/items", json=body)

    def add_payment_to_cart(self, to, amount, *, note=None):
        """Put a payment to a person in the cart. They still confirm it on the checkout page."""
        body = {"to": to, "amount": amount}
        if note:
            body["note"] = note
        return self.request("POST", "/cart/items", json=body)

    def add_game_to_cart(self, game_id):
        """Put a Hyperfocus game in the cart."""
        return self.request("POST", "/cart/items", json={"game_id": game_id})

    def quote_directly(self, items):
        """What pay_directly would cost: ``{total, lines}``. items: ``[{"product_id": ...}, {"to": ..., "amount": ...}, {"game_id": ...}]``."""
        return self.request("POST", "/checkout/direct/quote", json={"items": items})

    def pay_directly(self, items, expected_total, *, idempotency_key=None):
        """Pay without the checkout page (needs Transfer Credits). The person is notified. Anything that bills later needs checkout
        (``checkout_required``). Keep the key and send it again on a retry: the same key never charges twice."""
        key = idempotency_key or uuid.uuid4().hex
        return self.request("POST", "/checkout/direct", json={"items": items, "expected_total": expected_total, "idempotency_key": key})

    def product_access(self, product_id):
        """Does this person have it? ``{owned, count, membership}``. The app managing the product can always ask; others need View Credits."""
        return self.request("GET", f"/products/{quote(str(product_id), safe='')}/access")

    def servers(self):
        """Legacy: Nookara-hosted servers that have not moved. Use ``Instance.servers()`` for Ember."""
        warnings.warn("Nookara-hosted chat is legacy and read-only; use Instance for Ember servers", DeprecationWarning, stacklevel=2)
        return self.get_chat_servers()["servers"]

    def server(self, sid):
        """Legacy: one Nookara-hosted server (read-only)."""
        warnings.warn("Nookara-hosted chat is legacy and read-only; use Instance for Ember servers", DeprecationWarning, stacklevel=2)
        return self.get_chat_servers_by_sid(sid=sid)

    def messages(self, cid, *, before=None, after=None, limit=50):
        """Legacy: history of a Nookara-hosted channel (read-only)."""
        warnings.warn("Nookara-hosted chat is legacy and read-only; use Instance for Ember servers", DeprecationWarning, stacklevel=2)
        return self.get_chat_channels_by_cid_messages(cid=cid, query={"before": before, "after": after, "limit": limit})

    def send_message(self, cid, message, *, reply_to=None, attachments=None):
        """Legacy: writes answer ``server_read_only``. Use ``Instance.send_message`` for Ember."""
        warnings.warn("Nookara-hosted chat is legacy and read-only; use Instance for Ember servers", DeprecationWarning, stacklevel=2)
        return self.post_chat_channels_by_cid_messages(cid=cid, json={"message": message, "reply_to": reply_to, "attachments": attachments or []})

    def send_dm(self, username, message):
        raise RuntimeError("Direct messages are end-to-end encrypted now, so plain text is refused. Use nookara.EncryptedDMs: it makes this client's keys and asks the person to approve it.")

    def lookup(self, username):
        """One public profile (GET /account/lookup/:username). Friends-only profiles are limited for non-friends."""
        return self.get_account_lookup_by_username(username=username)

    def lookup_many(self, usernames):
        """Public profiles of many people at once: {lower-case username: profile}.

        Same shape and privacy rules as ``lookup``; unknown or blocked names are left out. Sends one
        GET /account/lookup?u=... per 100 names (the server's limit).
        """
        names = list(dict.fromkeys(str(n).strip() for n in usernames if str(n).strip()))
        out = {}
        for i in range(0, len(names), 100):
            res = self.get_account_lookup(query={"u": ",".join(names[i:i + 100])})
            for user in (res or {}).get("users", []):
                out[str(user.get("username", "")).lower()] = user
        return out

    def members(self, sid, *, limit=None, offset=None):
        """Legacy: one page of a Nookara-hosted server's member list (``total`` / ``next_offset`` when paged)."""
        warnings.warn("Nookara-hosted chat is legacy and read-only; use Instance for Ember servers", DeprecationWarning, stacklevel=2)
        return self.get_chat_servers_by_sid_members(sid=sid, query={"limit": limit, "offset": offset})

    def can_reply_to_status(self, username):
        """{"can": True, "text": ...} or {"can": False, "reason": ...} (own, bot, no_status, friends_only, not_found)."""
        return self.get_im_status_reply_by_username(username=username)

    def reply_to_status(self, username, message):
        """DM `username` as a reply to their current custom status (the server rejects it with status_changed if it changed)."""
        info = self.can_reply_to_status(username)
        if not info.get("can"):
            raise ValueError("cannot reply to this status: %s" % info.get("reason"))
        return self.post_im_send(json={"to": username, "message": message, "status_reply": {"text": info["text"]}})

    def set_activity(self, name, *, key="python-client", ttl=600, **fields):
        return self.post_chat_presence_activity(json={**fields, "name": name, "key": key, "ttl": ttl})

    def clear_activity(self, key="python-client"):
        return self.delete_chat_presence_activity_by_key(key=key)

    def storage_get(self, storage_id, key):
        return self.get_storage_by_storageid_by_key(storageId=storage_id, key=key)["value"]

    def storage_set(self, storage_id, key, value):
        if not isinstance(value, str):
            raise TypeError("Storage values are strings; use json.dumps for objects")
        return self.put_storage_by_storageid_by_key(storageId=storage_id, key=key, json={"value": value})

    def notifications(self, *, unread=False, category=None, cursor=None, limit=None):
        """{"notifications": [...], "next_cursor": id or None, "unread": n}, newest first (up to 50 per page).

        title/body are plain text with **bold** as the only markup; never render them as HTML.
        """
        return self.get_account_notifications(query={"unread": 1 if unread else None, "category": category,
                                                     "cursor": cursor, "limit": limit})

    def unread_notifications(self):
        """The number for the bell."""
        return self.get_account_notifications_unread_count()["unread"]

    def mark_notifications_read(self, ids=None, *, all=False):
        """Mark these ids (or every notification with all=True) read. Returns {"success", "unread"}."""
        if all:
            return self.post_account_notifications_read(json={"all": True})
        return self.post_account_notifications_read(json={"ids": list(ids or [])})

    def mark_notifications_unread(self, ids):
        return self.post_account_notifications_unread(json={"ids": list(ids)})

    def delete_notification(self, notification_id):
        return self.delete_account_notifications_by_id(id=notification_id)

    def notification_settings(self):
        """[{key, label, description, icon, locked, staff, email, list}, ...]; locked ones are always on."""
        return self.get_account_notification_settings()["categories"]

    def set_notification_settings(self, prefs):
        """prefs = {"friends": {"list": True, "email": False}, ...}; locked and unknown categories are ignored."""
        return self.patch_account_notification_settings(json={"prefs": prefs})

    def upload_dm_file(self, path, *, destination="temp"):
        """Upload a file for a DM. destination="temp": Nookara's temporary storage (free; expires after a while
        nobody opens it, every load resets the clock). destination="account": your Nookara account storage (counts
        toward your storage quota, stays until you delete it; needs the Media Upload scope). Returns the attachment
        {url, type, name, size, width, height, ...}; temp uploads also carry expires and ttl_days."""
        if destination not in ("temp", "account"):
            raise ValueError('destination must be "temp" or "account"')
        op = self.post_chat_media_temp if destination == "temp" else self.post_chat_media_account
        return op(files={"file": path})["attachment"]

    def upload_destinations(self):
        """Where DM files can go: {choice, account: {...remaining}, temp: {max_mb, days}} (choice = your Ember setting)."""
        return self.get_chat_media_destinations()

    def game_downloads(self):
        return self.get_chat_game_downloads()

    def game_instances(self, sid):
        return self.get_chat_game_servers_by_sid_instances(sid=sid)

    def game_unlink(self, sid, iid):
        return self.delete_chat_game_servers_by_sid_instances_by_iid(sid=sid, iid=iid)

    def game_unclaimed(self, sid, *, q=None, tag=None, page=None):
        return self.get_chat_game_unclaimed(query={"sid": sid, "q": q, "tag": tag, "page": page})

    def game_claim(self, sid, cid=None, *, hint=None):
        body = {"sid": sid, **({"cid": cid} if cid else {}), **({"hint": hint} if hint else {})}
        return self.post_chat_game_claims(json=body)

    def game_claim_state(self, code):
        return self.get_chat_game_claims_by_code(code=code)

    def game_status(self, cid):
        return self.get_chat_game_channels_by_cid_status(cid=cid)

    def game_console(self, cid, *, before=None):
        return self.get_chat_game_channels_by_cid_console(cid=cid, query={"before": before})

    def game_exec(self, cid, command):
        return self.post_chat_game_channels_by_cid_console(cid=cid, json={"command": command})

    def game_audit(self, sid, *, before=None):
        return self.get_chat_game_servers_by_sid_audit(sid=sid, query={"before": before})

    def ember_session(self):
        """``GET /bonfire/session`` for any token: ``{granted, effective, disabled, not_granted, ...}``.
        ``granted`` is the mask the person approved, ``effective`` also drops what an admin switched off."""
        return self.get_bonfire_session()

    def granted_scopes(self):
        """The scope mask this token can use right now (approved and not switched off by an admin)."""
        return int(self.ember_session()["effective"])

    def scope_names(self):
        """Identifiers of the usable scopes, for example ``["PROFILE_READ", "CHAT"]``."""
        return _scope_names(self.granted_scopes())

    def has_scope(self, scope):
        """True when the token can use ``"CHAT"`` / ``"Chat Messaging"`` / ``2048``. One request per call; cache the result."""
        return _has_scope(self.granted_scopes(), scope)

    def require_scope(self, scope):
        """Raise ``ScopeError`` unless the token holds the scope (so you can show "log in again to use this")."""
        bit = scope_bit(scope)
        if not _has_scope(self.granted_scopes(), bit):
            raise ScopeError(403, {"error": "insufficient_scope", "required_scope": bit})
        return bit

    def ember_scopes(self):
        """What the official Ember apps ask for (public): ``[{id, bit, required: False, name, reason, ...}]``."""
        return self.get_bonfire_scopes_json()["scopes"]

    def instance_token(self, url):
        """Short-lived token for one instance (needs Chat). Hand it to that instance only."""
        return self.post_bonfire_instance_token(json={"instance": url})

    def signing_key(self):
        """The account's Ed25519 signing key (needs the Sign Messages scope). Keep it in memory."""
        return self.get_bonfire_signing_key()

    def ember_instances(self):
        return self.get_bonfire_instances()["instances"]

    def set_ember_instances(self, urls):
        """Replace the saved instance list with these URLs, in this order."""
        return self.put_bonfire_instances(json={"instances": [{"url": normalize_origin(u)} for u in urls]})["instances"]

    def sync_ember_instances(self, local_urls=()):
        """Union of the saved list (server order first) and local_urls; saves and returns it."""
        merged = []
        for url in [i["url"] for i in self.ember_instances()] + [normalize_origin(u) for u in local_urls]:
            if url not in merged:
                merged.append(url)
        return self.set_ember_instances(merged)

    def ember_default_instance(self):
        """The official server every account gets once (``GET /bonfire/instances`` -> ``default_instance``), or None."""
        return self.get_bonfire_instances()["default_instance"]

    def ember_default_joined(self, url=None):
        """Tell Nookara this client joined (or skipped) the official server, so other devices do not auto-join again."""
        return self.post_bonfire_instances_default_joined(json={"url": normalize_origin(url)} if url else {})["instances"]

    def ember_instance_prefs(self, url, *, muted=None, push=None):
        """Per-server push consent: ``muted=True`` mutes it, ``push=False`` stops offline-mention pushes."""
        body = {"url": normalize_origin(url), "muted": muted, "push": push}
        return self.patch_bonfire_instances_prefs(json={k: v for k, v in body.items() if v is not None})

    def ember_profiles(self, ids):
        """Current names and pictures of Nookara accounts (public, up to 100 ids): ``[{id, username, display_name, pfp}]``."""
        return self.get_bonfire_profiles(query={"ids": ",".join(str(i) for i in ids)})["profiles"]

    def ember_key(self, kid):
        """Public signing key by id (public): ``{kid, user_id, public_key, created_at, revoked_at}``."""
        return self.get_bonfire_keys_kid_by_kid(kid=kid)

    def ember_user_keys(self, user_id):
        """Every signing key of an account, revoked ones included (public)."""
        return self.get_bonfire_keys_user_by_userid(userId=user_id)["keys"]

    def inbox_mentions(self, *, before=None, limit=None):
        """Ember's Inbox, Mentions (needs Chat): messages from the last 30 days in your servers that mention you
        (``@name``, a reply to you, ``@everyone`` / ``@here``, one of your roles), newest first.
        Returns ``{messages, has_more}``; each message has ``channel_name``, ``server_name``, ``server_icon`` and
        ``unread``. ``before`` is a message id for the next page; ``limit`` is 1 to 50 (default 30)."""
        return self.get_chat_inbox_mentions(query={"before": before, "limit": limit})

    def saved_messages(self, *, before=None, limit=None):
        """Your saved messages, newest first (needs Chat): ``{saved: [{id, kind, saved_at, message?, with?,
        missing?, hidden?}], has_more}``. ``kind`` is ``channel``, ``dm`` or ``group``. ``missing`` means the
        original is gone or you lost access; ``hidden`` is a saved DM this token may not read (no Read Instant
        Messages). ``before`` is a saved id; ``limit`` is 1 to 100 (default 50)."""
        return self.get_chat_saved(query={"before": before, "limit": limit})

    def save_message(self, kind, message_id=None, *, snapshot=None):
        """Save a message and return its saved id. ``kind="channel"``: ``message_id`` is a channel message id.
        ``kind="dm"``: ``message_id`` is the DM id (needs Read Instant Messages). ``kind="group"``: pass
        ``snapshot={room, room_name, user, message, created_at, id}`` instead. At most 500 saved
        (``APIError`` with ``too_many_saved``)."""
        if kind not in ("channel", "dm", "group"):
            raise ValueError("kind must be channel, dm or group")
        if kind == "group":
            if not snapshot:
                raise ValueError("a group message needs a snapshot")
            body = {"kind": kind, "snapshot": snapshot}
        else:
            if message_id is None:
                raise ValueError("message_id is required")
            body = {"kind": kind, "id": str(message_id)}
        return self.post_chat_saved(json=body)["id"]

    def unsave_message(self, saved_id):
        """Remove a saved message by its saved id (what ``save_message`` returned)."""
        return self.delete_chat_saved_by_id(id=saved_id)

    def saved_ids(self, kind, ids):
        """Which of these messages are saved? ``{message id: saved id}``; unsaved ones are left out (200 ids at most)."""
        return self.post_chat_saved_check(json={"kind": kind, "ids": [str(i) for i in ids]})["saved"]

    def translate(self, text, to="en", *, source=None):
        """Translate text on Nookara (needs Chat; 3000 characters, 40 a minute). ``to`` is a language tag such as
        ``"en"`` or ``"pt-BR"``; ``source`` is optional (detected). Returns ``{text, from, to}``."""
        return self.post_chat_translate(json={"text": text, "to": to, "from": source} if source else {"text": text, "to": to})

    def cancel_friend_request(self, username):
        """Take back a friend request you sent that hasn't been answered (needs View Friends and Manage Friends).
        Returns True, or False when there was no pending request to that person."""
        name = str(username).strip().lower()
        for req in self.get_friends_requests().get("outgoing", []):
            if str(req.get("to_username", "")).lower() == name:
                self.delete_friends_request_by_id(id=req["id"])
                return True
        return False

    def ember_beta(self):
        """Do you have Ember Beta? (needs Chat). Returns ``{beta, membership, product}``: ``beta`` is True only with a
        live active or trialing membership of the Ember Beta product (selling it doesn't count), ``membership`` is
        ``{status, period, current_period_end, cancel_at_period_end, test}`` or None, ``product`` is the public
        product view or None. The server caches the answer for 30 seconds."""
        return self.get_chat_beta()

    def refresh_ember_beta(self):
        """Same answer as ``ember_beta()`` but skips the 30 second cache (use it right after a purchase or a cancel)."""
        return self.post_chat_beta_refresh()

    def channel_viewers(self, cid):
        """Who can see a channel (needs Chat), for a member list. You must be able to see the channel yourself
        (otherwise 404). Returns ``{"all": True}`` when nothing limits who sees it, or ``{"all": False, "ids": [...]}``
        with the user ids (strings) of the server members who can (role overwrites, private channels, game console
        channels; owners, admins and Manage channels always see)."""
        return self.get_chat_channels_by_cid_viewers(cid=cid)

    def ember_jwks(self):
        """Nookara's identity keys (JWKS), used to verify instance tokens, receipts and bot-add tickets."""
        return self.get_well_known_bonfire_jwks_json()

    def server_latest(self):
        """The official bonfire-server build instances compare themselves with (public)."""
        return self.get_bonfire_server_latest_json()

    def ember_payout(self, url):
        """Who is paid for role-shop purchases on an instance you own."""
        return self.get_bonfire_instances_payout(query={"url": normalize_origin(url)})

    def ember_import_platforms(self):
        """Discord / Fluxer import sources and whether your account is linked: ``[{id, name, ready, bot, invite, linked}]``."""
        return self.get_bonfire_import_platforms()["platforms"]

    def ember_import_guilds(self, platform):
        return self.get_bonfire_import_by_platform_guilds(platform=platform)["guilds"]

    def start_ember_import(self, platform, guild_id, channels, instance, *, roles=(), options=None):
        """Build an import bundle on Nookara. Returns ``{job_id, ticket, instance, expires_at}``; the ticket goes to
        ``Instance.import_from_nookara``. The bundle has channels, roles and emoji, no members or messages."""
        body = {"platform": platform, "guild_id": guild_id, "channels": list(channels), "roles": list(roles),
                "instance": normalize_origin(instance)}
        if options:
            body["options"] = options
        return self.post_bonfire_import(json=body)

    def ember_import_job(self, job_id):
        return self.get_bonfire_import_by_job_id(job_id=job_id)

    def ember_directory(self, q=None, page=None):
        """Public directory of listed instances; no sign-in needed."""
        return self.get_bonfire_directory(query={"q": q, "page": page})

    def featured_projects(self, q=None, *, service=None, featured=None, limit=None, offset=None):
        """{"total", "limit", "offset", "projects": [...]}: approved projects, featured first. service = a key from
        project_services(); featured=True only featured ones; limit 1-100 (default 60). Text fields are plain text."""
        return self.request("GET", "/api/projects", query={"q": q, "service": service, "featured": 1 if featured else None,
                                                           "limit": limit, "offset": offset}, auth=False)

    def featured_project(self, slug):
        """One project by its slug: {"project": {...}}. With the submitter's token a project that isn't approved shows too."""
        return self.request("GET", "/api/projects/" + quote(str(slug), safe=""))

    def project_services(self):
        """[{"key": "login", "label": "Sign in with Nookara"}, ...]"""
        return self.request("GET", "/api/projects/services", auth=False)["services"]

    def my_projects(self):
        """Your submissions in every state (pending / approved / rejected with reject_reason / hidden)."""
        return self.request("GET", "/api/projects/mine")["projects"]

    def submit_project(self, title, tagline, url, services, *, description=None, icon=None, cover=None):
        """Send a project for review (pending). url must be https; icon / cover are a data:image URI or an https image link."""
        body = {"title": title, "tagline": tagline, "url": url, "services": list(services),
                "description": description, "icon": icon, "cover": cover}
        return self.request("POST", "/api/projects", json={k: v for k, v in body.items() if v is not None})

    def list_gallery(self, q=None, *, tag=None, page=None):
        """Public gallery of approved (verified) bots, 24 per page, most trusted first. No sign-in needed."""
        return self.get_bonfire_bots_gallery(query={"q": q, "tag": tag, "page": page})

    def gallery_tags(self):
        """Top 50 tags with the number of approved bots: ``[{"tag": "music", "count": 3}]``."""
        return self.get_bonfire_bots_gallery_tags()["tags"]

    def gallery_bot(self, bot_id):
        """Public detail of an approved bot. With the owner's (or staff) token an unlisted bot shows too, with its state."""
        return self.get_bonfire_bots_gallery_by_id(id=bot_id)

    def gallery_status(self, bot_id):
        """Owner view: ``{"gallery": {state, review_message, can_submit, can_withdraw, ...}, "log": [...]}``.
        ``state`` is private, pending, approved, rejected, delisted or banned."""
        return self.get_chat_bots_by_id_gallery(id=bot_id)

    def save_gallery_listing(self, bot_id, *, long_description=None, tags=None, support_url=None, links=None, permissions=None):
        """Save the listing fields without changing the review state (live at once for an approved bot)."""
        return self.put_chat_bots_by_id_gallery(id=bot_id, json=self._gallery_fields(long_description, tags, support_url, links, permissions))

    def submit_to_gallery(self, bot_id, *, long_description=None, tags=None, support_url=None, links=None, permissions=None):
        """Submit (or resubmit after a rejection / delisting) for review. The state becomes ``pending``.
        The bot needs a description of at least 10 characters and an avatar; the listing fields are optional and saved first."""
        return self.post_chat_bots_by_id_gallery_submit(id=bot_id, json=self._gallery_fields(long_description, tags, support_url, links, permissions))

    def resubmit_to_gallery(self, bot_id, **fields):
        """Alias of submit_to_gallery for a rejected or delisted bot."""
        return self.submit_to_gallery(bot_id, **fields)

    def withdraw_from_gallery(self, bot_id):
        """Back to ``private``. Servers that already have the bot keep it."""
        return self.post_chat_bots_by_id_gallery_withdraw(id=bot_id)

    def gallery_ticket(self, bot_id, instance):
        """Single-use add-ticket (5 minutes) for adding a listed bot to a server on ``instance``.
        Pass the ticket to ``Instance.add_gallery_bot(ticket, sid)``."""
        return self.post_bonfire_bots_gallery_by_id_ticket(id=bot_id, json={"instance": instance})

    @staticmethod
    def _gallery_fields(long_description, tags, support_url, links, permissions):
        fields = {"long_description": long_description, "tags": tags, "support_url": support_url, "links": links, "permissions": permissions}
        return {k: v for k, v in fields.items() if v is not None}

    def bot_installs(self):
        """For a *bot program* (``Client(bot_token, auth_scheme="Bot")``): the Ember instances this Nookara bot is
        installed on, ``[{origin, name, test, added_at, seen_at}]``. Open one ``Instance(origin, bot_token=...)`` bot
        gateway per entry (see ``BotProgram``) and poll again every few minutes."""
        return self.get_bonfire_bots_self_installs()["instances"]

    def hosting_plans(self):
        return self.get_bonfire_hosting_plans()

    def hosting_slug_available(self, slug):
        return self.get_bonfire_hosting_slug_by_slug(slug=slug)

    def hosting_servers(self):
        return self.get_bonfire_hosting_servers()

    def hosting_server_by_url(self, url):
        return self.get_bonfire_hosting_servers_by_url(query={"url": url})["server"]

    def create_hosting_server(self, slug, name, plan="starter", *, weeks=None, restore_backup=None):
        """Create a Nookara-hosted Ember server (e-<slug>.nookara.cc). Plus is prepaid in weeks."""
        body = {"slug": slug, "name": name, "plan": plan, "weeks": weeks, "restore_backup": restore_backup}
        return self.post_bonfire_hosting_servers(json={k: v for k, v in body.items() if v is not None})

    def buy_hosting_weeks(self, slug, weeks):
        return self.post_bonfire_hosting_servers_by_slug_weeks(slug=slug, json={"weeks": weeks})

    def set_hosting_plan(self, slug, plan="starter"):
        """Switch to the free plan. Upgrading to Plus is buy_hosting_weeks()."""
        return self.patch_bonfire_hosting_servers_by_slug(slug=slug, json={"plan": plan})

    def restart_hosting_server(self, slug):
        return self.post_bonfire_hosting_servers_by_slug_restart(slug=slug)

    def backup_hosting_server(self, slug):
        return self.post_bonfire_hosting_servers_by_slug_backup(slug=slug)["backup"]

    def delete_hosting_server(self, slug):
        """Backs the server up, then removes it. The name stays yours for 30 days."""
        return self.delete_bonfire_hosting_servers_by_slug(slug=slug, json={"confirm": slug})

    def hosting_backups(self):
        return self.get_bonfire_hosting_backups()["backups"]

    def download_hosting_backup(self, backup_id):
        return self.get_bonfire_hosting_backups_by_id_download(id=backup_id, raw=True)

    def upload_hosting_backup(self, path, name, url, *, slug=None):
        data = {"name": name, "url": url, "slug": slug}
        return self.post_bonfire_hosting_backups_upload(data=data, files={"file": path})["backup"]

    def delete_hosting_backup(self, backup_id):
        return self.delete_bonfire_hosting_backups_by_id(id=backup_id)


def login_app(app_id, *, port=0, timeout=300, on_url=None, base_url=BASE_URL, allow_insecure=False):
    """Sign in through a registered app (My Account > Apps). Returns ``(token, origin)``. Never asks for a password.

    The app needs ``http://localhost`` in its authorized URLs: the browser comes back to a small one-shot server on this
    computer with a one-time grant, which is swapped for the token. App tokens only work from the app's authorized URLs, so
    make your client with the origin this returns: ``Client(token, origin=origin)``. Outside a browser that header is
    only a promise, so keep the token as private as a password.
    """
    import http.server, threading
    from urllib.parse import parse_qs
    if not re.fullmatch(r"app_[0-9a-f]{20}", str(app_id)):
        raise ValueError("Use the app ID from My Account > Apps")
    got = {}
    page = (b"<!doctype html><title>Nookara</title><p>Signed in. You can close this tab.</p><script>"
            b"fetch('/done',{method:'POST',body:location.hash.slice(1)}).then(()=>{history.replaceState(null,'','/');});</script>")

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200); self.send_header("Content-Type", "text/html"); self.send_header("Content-Length", str(len(page))); self.end_headers()
            self.wfile.write(page)

        def do_POST(self):
            body = self.rfile.read(min(int(self.headers.get("Content-Length") or 0), 4096)).decode("ascii", "replace")
            got.update({k: v[0] for k, v in parse_qs(body).items()})
            self.send_response(204); self.end_headers()

        def log_message(self, *args):
            pass

    server = http.server.HTTPServer(("127.0.0.1", port), Handler)
    server.timeout = 1
    origin = "http://localhost:%d" % server.server_address[1]
    client = Client(base_url=base_url, allow_insecure=allow_insecure)
    try:
        code = client.request("POST", "/auth/ext-code", json={"app_id": app_id, "redirect_uri": origin + "/signed-in"}, auth=False)["code"]
        url = base_url.rstrip("/") + "/login?" + urlencode({"code": code})
        if on_url:
            on_url(url)
        else:
            webbrowser.open(url)
        deadline = time.monotonic() + min(timeout, 300)
        while time.monotonic() < deadline and "nookara_grant" not in got:
            server.handle_request()
    finally:
        server.server_close()
    if got.get("nookara_code") != code or "nookara_grant" not in got:
        raise TimeoutError("Nookara sign-in was not completed before the authorization code expired")
    result = client.request("POST", "/auth/ext-code/exchange", json={"code": code, "grant": got["nookara_grant"]}, auth=False)
    return result["token"], origin


def login(*, project_name="Python Nookara client", scopes=2049, optional_scopes=0, timeout=300, on_url=None, base_url=BASE_URL):
    """Ask the user to approve a scoped token in their browser. Never asks for a password.

    ``scopes`` is the mask you *request* (``scope_mask("PROFILE_READ", "CHAT")`` is 2049). Nothing can be
    required any more: the person may untick any scope, so check what came back with
    ``Client(token).granted_scopes()`` and handle ``ScopeError``. ``optional_scopes`` is kept for old code and
    is simply merged into ``scopes``. Project names that start with ``Ember (`` are reserved for the official apps.
    """
    if not isinstance(scopes, int) or not isinstance(optional_scopes, int) or scopes < 0 or optional_scopes < 0:
        raise ValueError("Use integer scope masks")
    requested = scopes | optional_scopes
    if not 0 < requested <= 65535:
        raise ValueError("Request at least one supported scope (bits up to 32768)")
    if re.match(r"\s*bonfire\s*\(", project_name, re.I):
        raise ValueError("Project names starting with 'Ember (' are reserved for the official apps")
    client = Client(base_url=base_url)
    mask = requested << 16
    code = client.post_auth_ext_code(json={"project_name": project_name, "permissions_integer": mask})["code"]
    url = base_url.rstrip("/") + "/login?" + urlencode({"code": code, "project": project_name, "permissions": mask})
    if on_url:
        on_url(url)
    else:
        webbrowser.open(url)
    deadline = time.monotonic() + min(timeout, 300)
    while time.monotonic() < deadline:
        result = client.get_auth_ext_code_status(query={"code": code})
        if result.get("ready"):
            return result["token"]
        time.sleep(1.5)
    raise TimeoutError("Nookara sign-in was not completed before the authorization code expired")
