"""End-to-end encrypted direct messages for a third-party client (the nke1 format).

Nookara's DMs are encrypted on the device, so a token alone only gets locked messages. A client makes its
own keys and asks the person to link it: they approve it from Ember by entering a code. After that it reads
new DMs (old ones too if they tick that), sends signed DMs, and can be unlinked any time.

    from velora_api import login_app, EncryptedDMs

    client = login_app(...)                                 # needs the Direct Messages permission
    dms = EncryptedDMs(client, key_file="nookara-dms.json")
    if not dms.linked():
        code = dms.request_link()
        print("In Ember: Settings > Privacy > Approve a device, and enter", code)
        dms.wait_for_approval(code)
    dms.send("alice", "Hello!")
    for m in dms.messages("alice"):
        print(m["from"], dms.open(m))

key_file holds your private keys and the keys you've seen for other people. Protect it like a password.
The full format is at /guides#social and in docs/E2EE.md. Needs: pip install "nookara[signing]"
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json as _json
import os
import secrets
import time
from pathlib import Path
from urllib.parse import quote

from .client import APIError

_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def _load_crypto():
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import ec, utils
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    except ImportError as exc:
        raise RuntimeError('Encrypted DMs need the cryptography package: pip install "nookara[signing]"') from exc
    return InvalidSignature, hashes, serialization, ec, utils, AESGCM, HKDF


def b64(data):
    return base64.urlsafe_b64encode(bytes(data)).rstrip(b"=").decode()


def unb64(text):
    text = str(text)
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def kid_of(enc_pub):
    return b64(hashlib.sha256(unb64(enc_pub)).digest())[:22]


def link_code(enc_pub):
    digest = hashlib.sha256(unb64(enc_pub)).digest()
    code = "".join(_ALPHABET[b & 31] for b in digest[:10])
    return f"{code[:5]}-{code[5:]}"


def commit_of(key):
    return b64(hmac.new(key, b"nke1 commit", hashlib.sha256).digest())


def clients_text(user_id, account_kid, doc):
    def one(c):
        return ",".join([c["kid"], c["enc_pub"], c["sig_pub"], quote(c.get("label") or "", safe="-_.!~*'()"), c.get("app") or "", str(c.get("added_at") or 0), str(c.get("revoked_at") or 0)])
    return f"nke1 clients|{user_id}|{account_kid}|{doc['seq']}|" + ";".join(one(c) for c in doc.get("list") or [])


class KeyChanged(Exception):
    """Someone's key isn't the one you saw before. They may have started over, or someone may be listening in."""

    def __init__(self, username):
        super().__init__(f"{username}'s encryption key changed")
        self.username = username


class EncryptedDMs:
    def __init__(self, client, *, key_file=None, keys=None):
        self.client = client
        self._path = Path(key_file) if key_file else None
        self._c = _load_crypto()
        state = keys
        if state is None and self._path and self._path.exists():
            state = _json.loads(self._path.read_text(encoding="utf-8"))
        self.state = state or self._new_state()
        self._save()
        self._bundles = {}

    def _new_state(self):
        _, _, _, ec, _, _, _ = self._c
        enc, sig = ec.generate_private_key(ec.SECP256R1()), ec.generate_private_key(ec.SECP256R1())
        enc_pub = self._raw_public(enc)
        return {"enc_priv": enc.private_numbers().private_value.to_bytes(32, "big").hex(), "sig_priv": sig.private_numbers().private_value.to_bytes(32, "big").hex(),
                "enc_pub": enc_pub, "sig_pub": self._raw_public(sig), "kid": kid_of(enc_pub), "pins": {}}

    def _raw_public(self, private):
        _, _, serialization, _, _, _, _ = self._c
        return b64(private.public_key().public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint))

    def _save(self):
        if not self._path:
            return
        self._path.write_text(_json.dumps(self.state), encoding="utf-8")
        try:
            os.chmod(self._path, 0o600)
        except OSError:
            pass

    def _private(self, name):
        _, _, _, ec, _, _, _ = self._c
        return ec.derive_private_key(int(self.state[name], 16), ec.SECP256R1())

    @property
    def kid(self):
        return self.state["kid"]

    def request_link(self):
        """Ask to be linked. Returns the code the person enters in Ember. It lasts 10 minutes."""
        res = self.client.request("POST", "/im/keys/link", json={"enc_pub": self.state["enc_pub"], "sig_pub": self.state["sig_pub"]})
        if res["code"] != link_code(self.state["enc_pub"]):
            raise RuntimeError("The code Nookara answered doesn't match this client's key. Don't continue.")
        return res["code"]

    def wait_for_approval(self, code, *, timeout=600, every=3):
        """Blocks until the person approves. Returns True, or False if they denied it or the code ran out."""
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            try:
                got = self.client.request("GET", f"/im/keys/link/{quote(code)}")
            except APIError as exc:
                if exc.error == "link_not_found":
                    return False
                raise
            if got.get("state") == "approved":
                return True
            if got.get("state") == "denied":
                return False
            time.sleep(every)
        return False

    def linked(self):
        me = self.client.request("GET", "/im/keys/me")
        return any(c["kid"] == self.kid and not c.get("revoked_at") for c in (me.get("clients") or {}).get("list") or [])

    def bundle(self, username, *, fresh=False):
        """Their public keys, checked: the client list has to be signed by their key, and their key has to be the one you saw before."""
        key = username.lower()
        if not fresh and key in self._bundles:
            return self._bundles[key]
        b = self.client.request("GET", f"/im/keys/user/{quote(username)}")
        doc = b.get("clients") or {"seq": 0, "list": []}
        if doc.get("list") and not self._verify(b["sig_pub"], clients_text(b["user_id"], b["kid"], doc).encode(), b.get("clients_sig")):
            raise RuntimeError(f"{username}'s client list isn't signed by their key. Don't send to it.")
        fp = b64(hashlib.sha256(unb64(b["enc_pub"]) + unb64(b["sig_pub"])).digest())
        pin = self.state["pins"].get(str(b["user_id"]))
        if pin and pin["fp"] != fp:
            raise KeyChanged(username)
        if pin and pin["seq"] > doc.get("seq", 0):
            raise RuntimeError(f"{username}'s client list is older than one already seen.")
        self.state["pins"][str(b["user_id"])] = {"fp": fp, "seq": doc.get("seq", 0)}
        self._save()
        self._bundles[key] = b
        return b

    def trust_new_key(self, username):
        """Accept a changed key (after KeyChanged), once you've checked with them some other way."""
        b = self.client.request("GET", f"/im/keys/user/{quote(username)}")
        self.state["pins"].pop(str(b["user_id"]), None)
        self._bundles.pop(username.lower(), None)
        self._save()
        return self.bundle(username)

    def _verify(self, sig_pub, data, signature):
        invalid, hashes, _, ec, utils, _, _ = self._c
        try:
            raw = unb64(signature)
            ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), unb64(sig_pub)).verify(
                utils.encode_dss_signature(int.from_bytes(raw[:32], "big"), int.from_bytes(raw[32:], "big")), data, ec.ECDSA(hashes.SHA256()))
            return True
        except (invalid, ValueError, TypeError):
            return False

    def _seal(self, secret, enc_pub, kid):
        _, hashes, _, ec, _, AESGCM, HKDF = self._c
        eph = ec.generate_private_key(ec.SECP256R1())
        eph_raw = unb64(self._raw_public(eph))
        shared = eph.exchange(ec.ECDH(), ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), unb64(enc_pub)))
        wrap = HKDF(algorithm=hashes.SHA256(), length=32, salt=eph_raw, info=f"nke1 wrap|{kid}".encode()).derive(shared)
        iv = secrets.token_bytes(12)
        return {"e": b64(eph_raw), "i": b64(iv), "w": b64(AESGCM(wrap).encrypt(iv, secret, None))}

    def _unseal(self, wrap, kid=None):
        _, hashes, _, ec, _, AESGCM, HKDF = self._c
        kid = kid or self.kid
        eph_raw = unb64(wrap["e"])
        shared = self._private("enc_priv").exchange(ec.ECDH(), ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), eph_raw))
        key = HKDF(algorithm=hashes.SHA256(), length=32, salt=eph_raw, info=f"nke1 wrap|{kid}".encode()).derive(shared)
        return AESGCM(key).decrypt(unb64(wrap["i"]), unb64(wrap["w"]), None)

    def encrypt(self, from_id, to_id, recipients, payload, *, edit_of=0):
        _, hashes, _, ec, utils, AESGCM, _ = self._c
        key, iv = secrets.token_bytes(32), secrets.token_bytes(12)
        body = _json.dumps({**payload, "n": b64(secrets.token_bytes(8))}, ensure_ascii=False).encode()
        ct, iv_s, commit = b64(AESGCM(key).encrypt(iv, body, f"nke1|{from_id}|{to_id}".encode())), b64(iv), commit_of(key)
        der = self._private("sig_priv").sign(f"nke1 sig|{from_id}|{to_id}|{edit_of}|{iv_s}|{ct}|{commit}".encode(), ec.ECDSA(hashes.SHA256()))
        r, s = utils.decode_dss_signature(der)
        return {"v": 1, "ct": ct, "iv": iv_s, "commit": commit, "sig": b64(r.to_bytes(32, "big") + s.to_bytes(32, "big")), "signer": self.kid,
                "wraps": {x["kid"]: self._seal(key, x["enc_pub"], x["kid"]) for x in recipients}}

    @staticmethod
    def _active(b):
        return [{"kid": b["kid"], "enc_pub": b["enc_pub"]}] + [{"kid": c["kid"], "enc_pub": c["enc_pub"]} for c in (b.get("clients") or {}).get("list") or [] if not c.get("revoked_at")]

    def open(self, message):
        """The text of a message from the API. None when this client wasn't given its key. Files stay as #nke= links in the text."""
        enc = message.get("enc")
        if not enc:
            return message.get("body")
        payload = self.open_payload(message)
        return None if payload is None else payload.get("t", "")

    def open_payload(self, message):
        """The whole opened message: t (text), r (quoted reply)."""
        _, _, _, _, _, AESGCM, _ = self._c
        enc = message["enc"]
        wrap = (enc.get("wraps") or {}).get(self.kid)
        if not wrap:
            return None
        key = self._unseal(wrap)
        if commit_of(key) != enc.get("commit"):
            return None
        plain = AESGCM(key).decrypt(unb64(enc["iv"]), unb64(enc["ct"]), f"nke1|{message['from_id']}|{message['to_id']}".encode())
        return _json.loads(plain)

    def signature_ok(self, message, bundle):
        """Was it signed by that person's key or one of their linked clients? bundle = self.bundle(sender)."""
        enc = message["enc"]
        if not enc.get("sig"):
            return False
        keys = {bundle["kid"]: bundle["sig_pub"], **{c["kid"]: c["sig_pub"] for c in (bundle.get("clients") or {}).get("list") or []}, **{p["kid"]: p["sig_pub"] for p in bundle.get("past") or []}}
        key = keys.get(enc.get("signer"))
        edit_of = message["id"] if message.get("edited_at") else 0
        text = f"nke1 sig|{message['from_id']}|{message['to_id']}|{edit_of}|{enc['iv']}|{enc['ct']}|{enc['commit']}"
        return bool(key) and self._verify(key, text.encode(), enc["sig"])

    def send(self, username, text, *, reply_to=None, reply_quote=None):
        """Send a DM. Raises APIError recipient_no_keys / no_keys if they haven't set up encrypted DMs yet."""
        for attempt in (0, 1):
            me = self.client.request("GET", "/im/keys/me")
            to = self.bundle(username, fresh=bool(attempt))
            payload = {"t": str(text)}
            if reply_quote:
                payload["r"] = reply_quote
            enc = self.encrypt(me["user_id"], to["user_id"], self._active(to) + self._active(me), payload)
            try:
                return self.client.request("POST", "/im/send", json={"to": username, "enc": enc, **({"reply_to": reply_to} if reply_to else {})})
            except APIError as exc:
                if exc.error != "stale_keys" or attempt:
                    raise
        return None

    def messages(self, username, *, before=None, limit=50):
        query = {"limit": limit, **({"before": before} if before else {})}
        return self.client.request("GET", f"/im/with/{quote(username)}", query=query).get("messages", [])
