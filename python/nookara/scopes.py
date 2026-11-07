"""Nookara token scopes and Ember instance scopes.

Scopes are *requested*, never required. The person signing in sees a consent screen and
may untick any of them (the risky ones start unticked), so a token can come back with
fewer scopes than you asked for. Ask only for what a feature needs, check what you got
with ``Client.granted_scopes()`` / ``Client.has_scope()`` and degrade gracefully.
"""
from __future__ import annotations


SCOPES = {
    "PROFILE_READ": 1,
    "PROFILE_SENSITIVE": 2,
    "PROJECT_AUTH": 4,
    "ACCOUNT_WRITE": 8,
    "STORAGE_READ": 16,
    "STORAGE_WRITE": 32,
    "VMAIL_READ": 64,
    "VMAIL_SEND": 128,
    "FRIENDS_READ": 256,
    "FRIENDS_MANAGE": 512,
    "CURRENCY_PAY": 1024,
    "CHAT": 2048,
    "MEDIA_UPLOAD": 4096,
    "CURRENCY_READ": 8192,
    "VOICE": 16384,
    "SIGN_MESSAGES": 32768,
}

SCOPE_LABELS = {
    "PROFILE_READ": "View Basic Profile",
    "PROFILE_SENSITIVE": "View Sensitive Info",
    "PROJECT_AUTH": "Project Auth",
    "ACCOUNT_WRITE": "Modify Settings",
    "STORAGE_READ": "Read Storage",
    "STORAGE_WRITE": "Write Storage",
    "VMAIL_READ": "Read Instant Messages",
    "VMAIL_SEND": "Send Instant Messages",
    "FRIENDS_READ": "View Friends",
    "FRIENDS_MANAGE": "Manage Friends",
    "CURRENCY_PAY": "Spend Credits",
    "CHAT": "Chat Messaging",
    "MEDIA_UPLOAD": "Upload Media",
    "CURRENCY_READ": "View Subscriptions",
    "VOICE": "Nookara Voice",
    "SIGN_MESSAGES": "Sign Messages",
}

DEFAULT_OFF = ("PROFILE_SENSITIVE", "ACCOUNT_WRITE", "STORAGE_WRITE", "FRIENDS_MANAGE", "CURRENCY_PAY", "SIGN_MESSAGES")

INSTANCE_SCOPES = {"chat": "CHAT", "voice": "VOICE", "media": "MEDIA_UPLOAD", "sign": "SIGN_MESSAGES"}

EMBER_APP_SCOPES = ("PROFILE_READ", "CHAT", "VMAIL_READ", "VMAIL_SEND", "FRIENDS_READ", "FRIENDS_MANAGE",
                      "MEDIA_UPLOAD", "VOICE", "ACCOUNT_WRITE", "CURRENCY_READ", "CURRENCY_PAY", "SIGN_MESSAGES")


def scope_bit(scope):
    """``"CHAT"``, ``"Chat Messaging"`` or ``2048`` -> ``2048``."""
    if isinstance(scope, int) and not isinstance(scope, bool):
        if scope <= 0 or scope & (scope - 1) or scope not in SCOPES.values():
            raise ValueError("Not a single scope bit: %r" % (scope,))
        return scope
    text = str(scope)
    key = text.upper().replace(" ", "_")
    if key in SCOPES:
        return SCOPES[key]
    for ident, label in SCOPE_LABELS.items():
        if label.lower() == text.lower():
            return SCOPES[ident]
    raise ValueError("Unknown scope: %r" % (scope,))


def scope_mask(*scopes):
    """Combine scope names (or bits) into the integer to request: ``scope_mask("PROFILE_READ", "CHAT") == 2049``."""
    mask = 0
    for s in scopes:
        mask |= scope_bit(s)
    return mask


def scope_names(mask):
    """Identifiers contained in a mask, lowest bit first: ``scope_names(2049) == ["PROFILE_READ", "CHAT"]``."""
    mask = int(mask)
    return [name for name, bit in SCOPES.items() if mask & bit == bit]


def has_scope(mask, scope):
    bit = scope_bit(scope)
    return int(mask) & bit == bit


def instance_scope_names(scopes):
    """Instance scope names (``chat``, ``voice``, ``media``, ``sign``) -> Nookara identifiers."""
    return [INSTANCE_SCOPES[s] for s in scopes if s in INSTANCE_SCOPES]


EMBER_APP_MASK = scope_mask(*EMBER_APP_SCOPES)
