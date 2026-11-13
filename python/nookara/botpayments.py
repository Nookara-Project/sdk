"""Bot payments: a bot asks a buyer for credits and polls for the result.

Authenticate with the bot token (``Authorization: Bot TOKEN``). The money goes to the bot's owner. The buyer
signs in on the Nookara pay page with their normal login; no scopes and no user token are ever involved, and
the bot never sees anything of the buyer's account. There is no webhook: poll with :meth:`BotClient.wait_for_payment`.

Never put a bot token into a Scratch/PenguinMod project, a web page or a mobile app: the PenguinMod Nookara
extension has no payment blocks for exactly this reason. Run this code on a server you control.
"""
from __future__ import annotations

import re
import time

from urllib.parse import quote

from .botdms import API_PREFIX, dm_error
from .client import BASE_URL, APIError, Client

FINAL_STATUSES = ("paid", "declined", "expired", "cancelled")
_ORDER_ID = re.compile(r"[A-Za-z0-9_.:-]{1,100}")


class PaymentError(APIError):
    """Any error answer of the bot payment API. ``error`` holds the server code (``invalid_amount``, ...)."""


class InvalidBotToken(PaymentError):
    """401 invalid_bot_token: the token is missing, wrong or was reset."""


class MerchantUnavailable(PaymentError):
    """403 merchant_unavailable or bot_banned: the owner account or the bot cannot take payments."""


class InvalidPaymentRequest(PaymentError):
    """400 validation: invalid_amount (``min``/``max`` in ``payload``), invalid_order_id, invalid_description,
    invalid_metadata, invalid_return_url, invalid_expires_in or invalid_buyer."""


class BuyerError(PaymentError):
    """buyer_not_found, buyer_is_bot, self_payment, buyer_banned, buyer_suspended, buyer_restricted."""


class OrderConflict(PaymentError):
    """409 order_id_conflict: the order_id exists with a different buyer or amount. Use a new order_id."""


class PaymentInProgress(PaymentError):
    """409 payment_in_progress: the buyer is paying right now, so the request cannot be cancelled."""


class NotCancellable(PaymentError):
    """409 not_cancellable: the request is already paid, declined or expired."""


class PaymentNotFound(PaymentError):
    """404 not_found: no such request for this bot."""


class PaymentRateLimited(PaymentError):
    """429 rate_limited, too_many_open_requests or buyer_has_too_many_open_requests (see ``retry_after``)."""


class PaymentTimeout(TimeoutError):
    """wait_for_payment ran out of time; the request is probably still pending. ``request`` is the last state."""

    def __init__(self, message, request=None):
        super().__init__(message)
        self.request = request


_BY_CODE = {
    "invalid_bot_token": InvalidBotToken,
    "merchant_unavailable": MerchantUnavailable, "bot_banned": MerchantUnavailable,
    "invalid_amount": InvalidPaymentRequest, "invalid_order_id": InvalidPaymentRequest,
    "invalid_description": InvalidPaymentRequest, "invalid_metadata": InvalidPaymentRequest,
    "invalid_return_url": InvalidPaymentRequest, "invalid_expires_in": InvalidPaymentRequest,
    "invalid_buyer": InvalidPaymentRequest,
    "buyer_not_found": BuyerError, "buyer_is_bot": BuyerError, "self_payment": BuyerError,
    "buyer_banned": BuyerError, "buyer_suspended": BuyerError, "buyer_restricted": BuyerError,
    "order_id_conflict": OrderConflict, "payment_in_progress": PaymentInProgress, "not_cancellable": NotCancellable,
    "not_found": PaymentNotFound,
    "rate_limited": PaymentRateLimited, "too_many_open_requests": PaymentRateLimited,
    "buyer_has_too_many_open_requests": PaymentRateLimited,
}


def payment_error(error):
    """Turn a plain :class:`APIError` into the matching :class:`PaymentError` subclass (same status and payload)."""
    cls = _BY_CODE.get(error.error) or (PaymentRateLimited if error.status == 429 else PaymentError)
    return cls(error.status, error.payload)


def is_paid(request):
    """True only for a request whose status is ``paid``. Also compare ``amount`` and ``buyer['id']`` with your order."""
    return bool(request) and request.get("status") == "paid"


def _id(value):
    text = str(value)
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", text):
        raise ValueError("Invalid payment request id")
    return text


def _dm_id(value):
    text = str(value)
    if not re.fullmatch(r"[0-9]{1,20}", text):
        raise ValueError("Invalid DM channel id")
    return text


class BotClient(Client):
    """A :class:`Client` that always authenticates as a bot (``Authorization: Bot TOKEN``) with the payment helpers."""

    def __init__(self, bot_token, *, base_url=BASE_URL, timeout=30, allow_insecure=False):
        if not bot_token:
            raise ValueError("A bot token is required")
        super().__init__(bot_token, base_url=base_url, auth_scheme="Bot", timeout=timeout, allow_insecure=allow_insecure)

    def __repr__(self):
        return f"BotClient(base_url={self.base_url!r})"

    # ---- DMs (0.9.8): Discord-shaped bot API on Nookara, /chat/api/v1 ----
    def _dm(self, method, path, **kwargs):
        try:
            return self.request(method, API_PREFIX + path, **kwargs)
        except APIError as error:
            raise dm_error(error) from None

    def open_dm(self, user_id=None, username=None):
        """Open (or get) a DM with a person: ``{"id": "1000000000012", "type": 1, "recipients": [user], "bonfire": {"dm": True, "with": name}}``.

        Give ``user_id`` or ``username``. The channel id is ``1000000000000`` + the user id (see :func:`dm_channel_id`), so
        you can skip this call for someone who wrote to you. Raises :class:`DMRefused` (``error`` is ``bot_no_shared_server``,
        ``dm_privacy``, ``bot_dms_off``, ``cannot_dm_bot`` or ``user_blocked``; ``detail`` is a sentence), or ``APIError`` 404
        ``user_not_found``. A bot may start a DM only when it shares an Ember server with the person and their "who can DM me"
        is everyone or servers; it may always answer someone who wrote to it first.
        """
        if (user_id is None) == (username is None):
            raise ValueError("Give user_id or username")
        body = {"recipient_id": str(user_id)} if user_id is not None else {"username": str(username).lstrip("@")}
        return self._dm("POST", "/users/@me/channels", json=body)

    def send_dm_message(self, channel_id, content, reply_to=None):
        """Send a plain-text DM into a channel from :meth:`open_dm` (never encrypted, no file attachments, ``<@id>`` becomes ``@name``).
        ``reply_to`` is a message id. Limits: 30 messages a minute, 20 new conversations an hour, 100 a day (``APIError`` 429 with ``retry_after``)."""
        body = {"content": str(content)}
        if reply_to is not None:
            body["message_reference"] = {"message_id": str(reply_to)}
        return self._dm("POST", f"/channels/{_dm_id(channel_id)}/messages", json=body)

    def dm_history(self, channel_id, *, before=None, after=None, limit=50):
        """DM messages, newest first (``limit`` 1 to 100). ``before`` / ``after`` are message ids."""
        return self._dm("GET", f"/channels/{_dm_id(channel_id)}/messages", query={"before": before, "after": after, "limit": limit})

    def dm_message(self, channel_id, message_id):
        """One DM message."""
        return self._dm("GET", f"/channels/{_dm_id(channel_id)}/messages/{_dm_id(message_id)}")

    def edit_dm_message(self, channel_id, message_id, content):
        """Edit one of the bot's own DM messages."""
        return self._dm("PATCH", f"/channels/{_dm_id(channel_id)}/messages/{_dm_id(message_id)}", json={"content": str(content)})

    def delete_dm_message(self, channel_id, message_id):
        """Delete one of the bot's own DM messages."""
        return self._dm("DELETE", f"/channels/{_dm_id(channel_id)}/messages/{_dm_id(message_id)}")

    def dm_typing(self, channel_id):
        """Show the typing indicator in a DM."""
        return self._dm("POST", f"/channels/{_dm_id(channel_id)}/typing", json={})

    def dm_channel(self, channel_id):
        """The DM channel object."""
        return self._dm("GET", f"/channels/{_dm_id(channel_id)}")

    def gateway(self, **kwargs):
        """The bot gateway on Nookara (``wss://nookara.cc/chat/gateway``): ``MESSAGE_CREATE`` / ``MESSAGE_UPDATE`` /
        ``MESSAGE_DELETE`` also arrive for DMs, with no ``guild_id`` and ``bonfire.dm`` set (see :func:`is_dm_event`; the
        events carry a ``dm`` flag too). Use ``async with bot.gateway() as gw``, ``async for event in gw`` or ``gw.on(...)`` + ``gw.run()``.
        Takes the ``BotGateway`` options (``reconnect``, ``timeout``, ...)."""
        from .instance import Instance
        from .instance_gateway import BotGateway
        return BotGateway(Instance(self.base_url, bot_token=self.token, allow_insecure=self.base_url.startswith("http://")),
                          path="/chat/gateway", **kwargs)

    def _pay(self, method, path, **kwargs):
        try:
            return self.request(method, path, **kwargs)
        except APIError as error:
            if isinstance(error, PaymentError):
                raise
            raise payment_error(error) from None

    def create_payment_request(self, buyer, amount, order_id, *, description=None, return_url=None, expires_in=None, metadata=None):
        """Ask ``buyer`` (a Nookara username or numeric id) for ``amount`` credits (1 to 10000).

        ``order_id`` is yours, unique per bot (letters, digits and ``_.:-``, up to 100). The result holds ``pay_url``:
        send the buyer there. Repeating the same order_id, buyer and amount returns the existing request with
        ``idempotent_replay`` true (whatever its status); a different buyer or amount raises :class:`OrderConflict`.
        ``return_url`` must be https; ``expires_in`` is 60 to 86400 seconds (default 3600); ``metadata`` (up to 500
        characters) comes back to you only and is never shown to the buyer.
        """
        if isinstance(amount, bool) or not isinstance(amount, int) or amount < 1:
            raise ValueError("amount must be a whole number of credits, at least 1")
        if not isinstance(order_id, str) or not _ORDER_ID.fullmatch(order_id):
            raise ValueError("order_id must be 1 to 100 characters of letters, digits and _ . : -")
        if buyer is None or str(buyer).strip() == "":
            raise ValueError("buyer is required")
        body = {"buyer": str(buyer).strip(), "amount": amount, "order_id": order_id}
        for key, value in (("description", description), ("return_url", return_url), ("expires_in", expires_in), ("metadata", metadata)):
            if value is not None:
                body[key] = value
        return self._pay("POST", "/bot/payment-requests", json=body)

    def get_payment_request(self, request_id):
        """One request of this bot by its ``bpr_...`` id. Raises :class:`PaymentNotFound` for anything else."""
        return self._pay("GET", "/bot/payment-requests/" + _id(request_id))

    def find_payment_request(self, order_id):
        """The request with this ``order_id``, or ``None`` when there is none."""
        try:
            return self._pay("GET", "/bot/payment-requests", query={"order_id": order_id})
        except PaymentNotFound:
            return None

    def list_payment_requests(self, status=None, *, limit=None):
        """Your latest requests (newest first), optionally only ``status`` (pending, paid, declined, expired, cancelled)."""
        if status is not None and status not in ("pending",) + FINAL_STATUSES:
            raise ValueError("status must be pending, paid, declined, expired or cancelled")
        return (self._pay("GET", "/bot/payment-requests", query={"status": status, "limit": limit}) or {}).get("requests", [])

    def cancel_payment_request(self, request_id):
        """Cancel a pending request (cancelling a cancelled one is fine). Raises :class:`PaymentInProgress` while the
        buyer is paying and :class:`NotCancellable` once it is paid, declined or expired."""
        return self._pay("POST", "/bot/payment-requests/" + _id(request_id) + "/cancel", json={})

    def create_cart(self, items, order_id, *, buyer=None, expires_in=None, return_url=None, metadata=None):
        """items: ``[{"product_id": "prod_...", "plan": "yearly", "quantity": 1}, {"amount": 20, "description": "Premium pack"}]``. Only your
        owner's products, and amounts go to your owner. buyer is optional: name someone and only they can pay. The same order_id returns the same cart."""
        body = {"items": items, "order_id": order_id}
        for key, value in (("buyer", buyer), ("expires_in", expires_in), ("return_url", return_url), ("metadata", metadata)):
            if value is not None:
                body[key] = value
        return self._pay("POST", "/bot/carts", json=body)

    def get_cart(self, cart_id):
        return self._pay("GET", f"/bot/carts/{quote(str(cart_id), safe='')}")

    def find_cart(self, order_id):
        return self._pay("GET", "/bot/carts", query={"order_id": order_id})

    def cancel_cart(self, cart_id):
        return self._pay("POST", f"/bot/carts/{quote(str(cart_id), safe='')}/cancel")

    def wait_for_cart(self, cart_id, timeout=900, poll=3.0, *, max_poll=15.0, sleep=time.sleep, clock=time.monotonic):
        """Poll until the cart is no longer open and return it. Give access only when ``status == "paid"``; ``buyer`` says who paid."""
        end = clock() + timeout
        wait = poll
        while True:
            cart = self.get_cart(cart_id)
            if cart.get("status") != "open":
                return cart
            if clock() + wait > end:
                return cart
            sleep(wait)
            wait = min(wait * 1.5, max_poll)

    def wait_for_payment(self, request_id, timeout=900, poll=3.0, *, max_poll=15.0, sleep=time.sleep, clock=time.monotonic):
        """Poll until the request is no longer pending and return it (check ``status``; use :func:`is_paid`).

        Polls every ``poll`` seconds, slowing down gently up to ``max_poll`` (the API has no webhook; reads are limited
        to 300 per minute per bot). Raises :class:`PaymentTimeout` after ``timeout`` seconds, with ``.request`` set.
        """
        deadline = clock() + timeout
        delay = max(0.1, float(poll))
        request = None
        while True:
            try:
                request = self.get_payment_request(request_id)
            except PaymentRateLimited as error:
                delay = max(delay, error.retry_after or delay)
            else:
                if request.get("status") in FINAL_STATUSES:
                    return request
            if clock() + delay > deadline:
                raise PaymentTimeout("payment still pending after %s seconds" % timeout, request)
            sleep(delay)
            delay = min(max_poll, delay * 1.25)
