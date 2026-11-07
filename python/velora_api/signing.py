"""Optional message signing (Bonfire protocol section 8).

Canonical JSON and payload building need nothing but the standard library.
Producing signatures needs the optional ``cryptography`` package
(``pip install nookara[signing]``).
"""
from __future__ import annotations

import base64
import json
import os
import time

PREFIX = "bonfire-msg-v1\n"


def b64url(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def b64url_decode(text):
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def canonical(value):
    """JSON with object keys sorted recursively, no whitespace, integer numbers."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        if isinstance(value, float) and (value != value or value in (float("inf"), float("-inf"))):
            raise ValueError("Non-finite number")
        return str(int(value))
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, (list, tuple)):
        return "[" + ",".join(canonical(v) for v in value) + "]"
    if isinstance(value, dict):
        return "{" + ",".join(json.dumps(k, ensure_ascii=False) + ":" + canonical(value[k]) for k in sorted(value)) + "}"
    raise TypeError("Cannot canonicalize " + type(value).__name__)


def normalize_body(text):
    """The instance stores bodies with CRLF folded to LF; sign exactly that text."""
    return str(text).replace("\r\n", "\n")


def build_payload(*, iss, instance, community, channel, author, ts, nonce, body,
                  attachments=(), reply_to=None, edit_of=None):
    return {
        "v": 1, "iss": iss, "instance": instance, "community": community, "channel": channel,
        "author": str(author), "ts": int(ts), "nonce": str(nonce), "body": normalize_body(body),
        "attachments": [str(a) for a in attachments],
        "reply_to": None if reply_to is None else str(reply_to),
        "edit_of": None if edit_of is None else str(edit_of),
    }


def signing_bytes(payload):
    return (PREFIX + canonical(payload)).encode("utf-8")


def attachment_refs(attachments):
    """What goes into the signed ``attachments`` list: the sha256 of each stored upload, or ``url:<url>`` for a
    link-only Klipy GIF that has no hash (the exact stored URL, 512 characters at most)."""
    refs = []
    for a in attachments or ():
        if not isinstance(a, dict):
            refs.append(str(a))
            continue
        sha = str(a.get("sha256") or "")
        if len(sha) == 64 and all(c in "0123456789abcdef" for c in sha):
            refs.append(sha)
        elif str(a.get("url") or "").startswith("https://") and ".klipy.com/" in str(a.get("url")).lower():
            refs.append("url:" + str(a["url"])[:512])
        else:
            raise ValueError("Attachment has no sha256; upload it through the instance first")
    return refs


def payload_from_message(message, *, iss, instance):
    """Rebuild the signed payload from a message as the instance returns it (``GET /channels/:cid/messages``).

    A message that was edited and still carries a signature was signed as an edit (``edit_of`` = its id)."""
    sig = message.get("signature") or {}
    author = message.get("author") or {}
    vid = author.get("velora_id") or (str(author.get("id", ""))[2:] if str(author.get("id", "")).startswith("v:") else None)
    if not sig or not vid:
        raise ValueError("Message is unsigned or has no Nookara author")
    return build_payload(iss=iss, instance=instance, community=message["server"], channel=message["channel"], author=vid,
                         ts=sig["ts"], nonce=sig["nonce"], body=message.get("body", ""),
                         attachments=attachment_refs(message.get("attachments")), reply_to=message.get("reply_to"),
                         edit_of=message["id"] if message.get("edited_at") else None)


def verify_message(message, key, *, iss, instance):
    """Check a signed message yourself instead of trusting its ``verified`` flag. Needs ``cryptography``.

    ``key`` is the public key record from Nookara (``Client.bonfire_key(message["signature"]["kid"])``).
    Returns ``(True, "ok")`` or ``(False, reason)`` with reason one of ``unsigned``, ``wrong_user``, ``revoked``,
    ``bad_key``, ``bad_signature`` or ``mismatch``.
    """
    sig = message.get("signature")
    if not sig:
        return False, "unsigned"
    try:
        payload = payload_from_message(message, iss=iss, instance=instance)
    except (ValueError, KeyError):
        return False, "mismatch"
    if str(key.get("user_id")) != payload["author"] or key.get("kid") != sig.get("kid"):
        return False, "wrong_user"
    if key.get("revoked_at") is not None and int(key["revoked_at"]) < payload["ts"]:
        return False, "revoked"
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    except ImportError:
        raise ImportError("Install nookara[signing] to verify messages") from None
    try:
        public = Ed25519PublicKey.from_public_bytes(b64url_decode(key["public_key"]))
    except (ValueError, KeyError):
        return False, "bad_key"
    try:
        public.verify(b64url_decode(sig["sig"]), signing_bytes(payload))
    except (InvalidSignature, ValueError):
        return False, "bad_signature"
    return True, "ok"


class Signer:
    """Holds the account's Ed25519 key in memory only. Never printed or stored."""

    def __init__(self, kid, private_key, *, iss, public_key=None):
        try:
            from cryptography.hazmat.primitives.serialization import load_der_private_key
        except ImportError:
            raise ImportError("Install nookara[signing] to sign messages") from None
        self.kid, self.iss, self.public_key = kid, iss, public_key
        self._key = load_der_private_key(b64url_decode(private_key), password=None)

    @classmethod
    def from_key_response(cls, response, *, iss):
        """Build from ``GET /bonfire/signing-key`` ({kid, public_key, private_key})."""
        return cls(response["kid"], response["private_key"], iss=iss, public_key=response.get("public_key"))

    def __repr__(self):
        return f"Signer(kid={self.kid!r})"

    def sign(self, **fields):
        """Return the ``signature`` object ``{kid, sig, ts, nonce}`` for a message.

        Pass instance, community, channel, author, body and optionally attachments
        (sha256 hex strings), reply_to, edit_of, ts and nonce.
        """
        ts = int(fields.pop("ts", None) or time.time() * 1000)
        nonce = fields.pop("nonce", None) or b64url(os.urandom(16))
        payload = build_payload(iss=self.iss, ts=ts, nonce=nonce, **fields)
        signature = self._key.sign(signing_bytes(payload))
        return {"kid": self.kid, "sig": b64url(signature), "ts": ts, "nonce": nonce}
