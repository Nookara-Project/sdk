"""Ember server permission numbers: a role's ``permissions``, your ``server.perms``, a channel's allow / deny.

Each permission is one bit; the number is all of them added up. These turn a number into names and back.
Calculator and the full list: https://nookara.cc/docs/ember-permissions

    >>> ember_permission_names(257)
    ['SEND', 'ATTACH']
    >>> ember_permission_mask("SEND", "ATTACH")
    257

Bits this version doesn't know come out as ``BIT_<n>`` and go back in the same way, so nothing is lost.
"""
from __future__ import annotations

# The table below is generated from ember-server's src/perms.js (VELORA scripts/ember-permissions/gen.js --sdk). Don't edit it by hand.
# gen:start
EMBER_PERMISSIONS = {
    "SEND": 1,
    "MANAGE_CHANNELS": 2,
    "MANAGE_SERVER": 4,
    "MANAGE_ROLES": 8,
    "KICK": 16,
    "BAN": 32,
    "MANAGE_MESSAGES": 64,
    "MENTION_EVERYONE": 128,
    "ATTACH": 256,
    "ADMIN": 512,
    "VIEW": 1024,
    "MANAGE_USERS": 2048,
    "UNMARKED_ALIASES": 4096,
}

EMBER_PERMISSION_LABELS = {
    "SEND": "Send messages",
    "MANAGE_CHANNELS": "Manage channels",
    "MANAGE_SERVER": "Manage server",
    "MANAGE_ROLES": "Manage roles",
    "KICK": "Kick members",
    "BAN": "Ban members",
    "MANAGE_MESSAGES": "Manage messages",
    "MENTION_EVERYONE": "Mention @everyone, @here and all roles",
    "ATTACH": "Attach files",
    "ADMIN": "Administrator",
    "VIEW": "View channel",
    "MANAGE_USERS": "Manage users",
    "UNMARKED_ALIASES": "Use unmarked aliases",
}

EMBER_ALL_PERMISSIONS = 7167
EMBER_CHANNEL_PERMISSIONS = 1281
EMBER_EVERYONE_DEFAULT = 257
# gen:end

_ALIASES = {"SEND_MESSAGES": "SEND", "KICK_MEMBERS": "KICK", "BAN_MEMBERS": "BAN", "ATTACH_FILES": "ATTACH",
            "ADMINISTRATOR": "ADMIN", "VIEW_CHANNEL": "VIEW", "UNMARKED_ALIAS": "UNMARKED_ALIASES"}


def _known():
    mask = 0
    for bit in EMBER_PERMISSIONS.values():
        mask |= bit
    return mask


def _number(value):
    if isinstance(value, bool):
        raise TypeError("Permissions must be a whole number, not %r" % (value,))
    if isinstance(value, int):
        number = value
    else:
        text = str(value).strip().replace("_", "")
        try:
            number = int(text, 0) if text else 0
        except ValueError:
            raise ValueError("Permissions must be a whole number, like 257: %r" % (value,)) from None
    if number < 0:
        raise ValueError("Permissions can't be negative: %r" % (value,))
    return number


def ember_permission_bit(permission):
    """``"SEND"``, ``"send messages"``, ``"Attach files"``, ``"BIT_13"`` or ``256`` -> its bit value."""
    if isinstance(permission, int) and not isinstance(permission, bool):
        if permission <= 0 or permission & (permission - 1):
            raise ValueError("Not a single permission bit: %r" % (permission,))
        return permission
    text = str(permission).strip()
    key = "_".join(text.upper().replace("-", " ").split())
    key = _ALIASES.get(key, key)
    if key in EMBER_PERMISSIONS:
        return EMBER_PERMISSIONS[key]
    for name, label in EMBER_PERMISSION_LABELS.items():
        if label.lower() == text.lower():
            return EMBER_PERMISSIONS[name]
    if key.startswith("BIT_") and key[4:].isdigit():
        return 1 << int(key[4:])
    raise ValueError("Unknown Ember permission: %r (see https://nookara.cc/docs/ember-permissions)" % (permission,))


def ember_permission_mask(*permissions):
    """Names (or bits) -> the number: ``ember_permission_mask("SEND", "ATTACH") == 257``. A single list works too."""
    if len(permissions) == 1 and isinstance(permissions[0], (list, tuple, set, frozenset)):
        permissions = tuple(permissions[0])
    mask = 0
    for p in permissions:
        mask |= ember_permission_bit(p)
    return mask


def ember_permission_names(value):
    """The number (int, or a string like ``"257"`` / ``"0x101"``) -> names, lowest bit first."""
    number = _number(value)
    names = [name for name, bit in EMBER_PERMISSIONS.items() if number & bit == bit]
    rest, bit = number & ~_known(), 0
    while rest:
        if rest & 1:
            names.append("BIT_%d" % bit)
        rest >>= 1
        bit += 1
    return names


def has_ember_permission(value, permission):
    """Does this number allow ``permission``? ADMIN counts as every permission, like the server does."""
    number, bit = _number(value), ember_permission_bit(permission)
    if number & EMBER_PERMISSIONS["ADMIN"] and bit & _known():
        return True
    return number & bit == bit
