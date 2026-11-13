"""Bot DMs (Nookara 2026-11): a bot opens a DM with a person, sends, reads history, edits and deletes its own messages.

A DM with a bot is ALWAYS plain text and never end-to-end encrypted (bots cannot hold keys), and a person can send one
from any client with ``Client.send_dm``. Bots use the Discord-shaped REST API on Nookara (``/chat/api/v1``) and the
gateway at ``wss://nookara.cc/chat/gateway``; see :meth:`BotClient.open_dm` and :meth:`BotClient.gateway`.

Rules a bot is held to: never another bot, never when its owner is 13-15, always OK to answer someone who wrote to it
first, otherwise it needs a shared Ember server and the person's "who can DM me" must be everyone or servers. Limits:
30 DM messages a minute, 20 new conversations an hour, 100 a day (429 with ``retry_after``).
"""
from __future__ import annotations

from .client import APIError

DM_CHANNEL_BASE = 1000000000000
API_PREFIX = "/chat/api/v1"
#: the ``error`` values of a refused DM (HTTP 403, Discord code 50007); ``payload["detail"]`` says it in words
DM_REFUSALS = ("bot_no_shared_server", "dm_privacy", "bot_dms_off", "cannot_dm_bot", "user_blocked")


class DMRefused(APIError):
    """403 50007: the bot may not DM this person (``error`` is one of :data:`DM_REFUSALS`; ``detail`` is a sentence to show)."""

    @property
    def detail(self):
        return self.payload.get("detail") if isinstance(self.payload, dict) else None


def dm_error(error):
    """Turn a plain :class:`APIError` into :class:`DMRefused` when it is a DM refusal (same status and payload)."""
    if error.status == 403 and (error.error in DM_REFUSALS or (isinstance(error.payload, dict) and error.payload.get("code") == 50007)):
        return DMRefused(error.status, error.payload)
    return error


def dm_channel_id(user_id):
    """The DM channel id for a user id (``1000000000000`` + id), without a request."""
    return str(DM_CHANNEL_BASE + int(user_id))


def dm_user_id(channel_id):
    """The user id a DM channel id is about, or ``None`` when it is not a DM channel id."""
    try:
        n = int(str(channel_id))
    except ValueError:
        return None
    return str(n - DM_CHANNEL_BASE) if n > DM_CHANNEL_BASE else None


def is_dm_event(event):
    """True for a bot-gateway ``MESSAGE_CREATE`` / ``MESSAGE_UPDATE`` / ``MESSAGE_DELETE`` that is a DM (no ``guild_id``,
    ``bonfire.dm`` set). Takes the ``{"type", "data"}`` event the gateway yields, or just its ``data``."""
    data = event.get("data", event) if isinstance(event, dict) else None
    if not isinstance(data, dict):
        return False
    if isinstance(event, dict) and "data" in event and not str(event.get("type", "")).startswith("MESSAGE_"):
        return False
    return not data.get("guild_id") and bool((data.get("bonfire") or {}).get("dm"))
