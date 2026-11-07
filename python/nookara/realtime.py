from __future__ import annotations

import asyncio
import json
import uuid
from contextlib import suppress

from .client import APIError

GAME_EVENT_TYPES = ("game_status", "game_console", "game_linked", "game_unlinked")
NOTIFICATION_EVENT_TYPES = ("notification_new", "notifications_updated")


class RealtimeClient:
    """User websocket protocol. REST and bot gateway clients are separate.

    Consume events continuously. rpc() matches nonce replies without dropping
    unrelated events. Reconnect explicitly, then refetch history; no replay exists.
    """

    def __init__(self, token, *, url="wss://nookara.cc/", timeout=30, allow_insecure=False):
        if not url.startswith("wss://") and not (allow_insecure and url.startswith("ws://")):
            raise ValueError("Use wss:// for a production websocket")
        self._token, self.url, self.timeout = token, url, timeout
        self._socket = None
        self._reader = None
        self._pending = {}
        self._events = asyncio.Queue(maxsize=256)
        self.auth = None

    async def __aenter__(self):
        if self._socket:
            raise RuntimeError("Already connected")
        try:
            from websockets.asyncio.client import connect
        except ImportError:
            raise ImportError("Install nookara[realtime] to use websockets") from None
        self._events = asyncio.Queue(maxsize=256)
        self._socket = await connect(self.url, open_timeout=self.timeout, max_size=8 * 1024 * 1024)
        try:
            await self._socket.send(json.dumps({"type": "auth_token", "token": self._token}))
            deadline = asyncio.get_running_loop().time() + self.timeout
            while True:
                remaining = deadline - asyncio.get_running_loop().time()
                frame = json.loads(await asyncio.wait_for(self._socket.recv(), max(0, remaining)))
                if frame.get("type") in ("auth_error", "auth_failed", "error"):
                    raise APIError(401, frame)
                if frame.get("type") == "auth_success":
                    if frame.get("tos_required"):
                        raise APIError(403, {"error": "tos_required"})
                    self.auth = frame
                    break
                self._events.put_nowait(frame)
            self._reader = asyncio.create_task(self._read())
            if self.auth.get("scopes", 0) & 2048:
                await self.send("chat_hello")
            return self
        except BaseException:
            await self.close()
            raise

    async def __aexit__(self, *args):
        await self.close()

    async def send(self, event_type, **fields):
        if not self._socket or (self._reader and self._reader.done()):
            raise ConnectionError("Nookara websocket is not connected")
        await self._socket.send(json.dumps({**fields, "type": event_type}, ensure_ascii=False))

    async def rpc(self, event_type, *, timeout=None, **fields):
        """Use only for events with a nonce reply, such as chat_send and RTC requests."""
        nonce = uuid.uuid4().hex
        future = asyncio.get_running_loop().create_future()
        self._pending[nonce] = future
        try:
            await self.send(event_type, **{**fields, "nonce": nonce})
            return await asyncio.wait_for(future, self.timeout if timeout is None else timeout)
        finally:
            self._pending.pop(nonce, None)

    async def send_message(self, channel, message, **fields):
        return await self.rpc("chat_send", channel=channel, message=message, **fields)

    async def set_activity(self, name, **fields):
        await self.send("set_rich_presence", activity={**fields, "name": name})

    async def clear_activity(self):
        await self.send("clear_rich_presence")

    async def watch_presence(self, usernames):
        """Ask for these people's presence (up to 200 per frame): one presence_bulk frame answers each batch, then this
        socket keeps receiving presence_update for them until it closes. Send it again after reconnecting."""
        names = list(dict.fromkeys(str(n) for n in usernames if n))
        for i in range(0, len(names), 200):
            await self.send("chat_presence_watch", usernames=names[i:i + 200])

    async def game_events(self):
        """Yield only Ember Link frames: game_status, game_console, game_linked, game_unlinked.

        Needs the Chat scope. This reads the same queue as plain iteration; use one or the other.
        """
        async for frame in self:
            if frame.get("type") in GAME_EVENT_TYPES:
                yield frame

    async def notification_events(self):
        """Yield only notification frames: notification_new and notifications_updated.

        notification_new = {notification, unread}; notifications_updated = {unread, read: [ids] or "all",
        unread_ids, deleted} (only the keys that apply). No scope needed. This reads the same queue as plain
        iteration; use one or the other. After a reconnect, refetch with Client.notifications().
        """
        async for frame in self:
            if frame.get("type") in NOTIFICATION_EVENT_TYPES:
                yield frame

    def __aiter__(self):
        return self

    async def __anext__(self):
        item = await self._events.get()
        if item is None:
            raise StopAsyncIteration
        if isinstance(item, Exception):
            raise item
        return item

    async def _read(self):
        failure = None
        try:
            async for raw in self._socket:
                if isinstance(raw, bytes):
                    self._events.put_nowait({"type": "binary", "data": raw})
                    continue
                frame = json.loads(raw)
                nonce = frame.get("nonce")
                future = self._pending.get(nonce)
                if future and not future.done():
                    if frame.get("type") in ("chat_error", "im_error", "error"):
                        future.set_exception(APIError(400, frame))
                    else:
                        future.set_result(frame)
                else:
                    self._events.put_nowait(frame)
        except asyncio.CancelledError:
            raise
        except asyncio.QueueFull:
            failure = RuntimeError("Nookara event queue is full; consume events continuously, then reconnect and resync")
            await self._socket.close()
        except Exception as exc:
            failure = exc
        finally:
            for future in self._pending.values():
                if not future.done():
                    future.set_exception(ConnectionError("Nookara websocket closed"))
            if self._events.full():
                self._events.get_nowait()
            self._events.put_nowait(failure)

    async def close(self):
        if self._reader:
            self._reader.cancel()
            with suppress(asyncio.CancelledError):
                await self._reader
            self._reader = None
        if self._socket:
            await self._socket.close()
            self._socket = None
