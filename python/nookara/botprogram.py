"""A bot program that serves every Ember server it is installed on.

A bot added from the Nookara bot gallery (or created on an instance) keeps ONE token. Each instance has its own
bot account and its own gateway, so a bot program opens one ``/bot/gateway`` connection per instance. Nookara
tells the program where it is installed: ``GET /bonfire/bots/self/installs`` with ``Authorization: Bot TOKEN``.

    async def main():
        async with BotProgram(os.environ["NOOKARA_BOT_TOKEN"]) as bot:
            async for event in bot:                    # {"instance", "type", "data", "seq"}
                if event["type"] == "MESSAGE_CREATE" and event["data"]["content"] == "!ping":
                    await bot.send(event["instance"], event["data"]["channel_id"], "pong")

Events are not replayed on reconnect: refetch what you need after a ``gateway_ready`` that follows a drop.
"""
from __future__ import annotations

import asyncio
import inspect
from contextlib import suppress

from ._origin import normalize_origin
from .client import APIError, Client, TransportError
from .instance import Instance


class BotProgram:
    """One bot token, many instances."""

    def __init__(self, token, *, nookara_url="https://nookara.cc", poll_interval=300.0, queue_size=2048,
                 include_test=False, allow_insecure=False, instance_factory=None, gateway_factory=None, timeout=30):
        self.token = token
        self.poll_interval, self.include_test = poll_interval, include_test
        self.allow_insecure, self.timeout = allow_insecure, timeout
        self._nookara = Client(token, base_url=nookara_url, auth_scheme="Bot", timeout=timeout, allow_insecure=allow_insecure)
        self._instance_factory = instance_factory or (lambda origin: Instance(origin, bot_token=token, timeout=timeout,
                                                                              allow_insecure=allow_insecure))
        self._gateway_factory = gateway_factory or (lambda inst: inst.bot_gateway())
        self._queue_size = queue_size
        self._events = None
        self._tasks = {}
        self._gateways = {}
        self._instances = {}
        self._poller = None
        self._handlers = {}
        self._closing = False
        self.errors = {}

    def installs(self):
        """The instances this bot is installed on right now (blocking call; test installs only with ``include_test``)."""
        items = self._nookara.bot_installs()
        out = []
        for item in items:
            if item.get("test") and not self.include_test:
                continue
            try:
                out.append(normalize_origin(item["origin"], allow_insecure=self.allow_insecure))
            except ValueError:
                continue
        return out

    @property
    def origins(self):
        return sorted(self._gateways)

    def instance(self, origin):
        """The bot-token ``Instance`` for one origin (REST helpers such as ``bot_send``)."""
        return self._instances[normalize_origin(origin, allow_insecure=self.allow_insecure)]

    def on(self, event_type, callback=None):
        def register(fn):
            self._handlers.setdefault(event_type, []).append(fn)
            return fn
        return register(callback) if callback else register

    async def start(self):
        if self._events is not None:
            raise RuntimeError("Already started")
        self._closing = False
        self._events = asyncio.Queue(maxsize=self._queue_size)
        await self.refresh()
        self._poller = asyncio.create_task(self._poll())
        return self

    async def refresh(self):
        """Fetch the install list and connect to new instances / drop removed ones."""
        try:
            wanted = set(await asyncio.to_thread(self.installs))
        except (APIError, TransportError) as exc:
            self._emit({"instance": None, "type": "installs_error", "data": {"error": getattr(exc, "error", "unreachable")}, "seq": None})
            return sorted(self._gateways)
        for origin in sorted(wanted - set(self._gateways)):
            await self._connect(origin)
        for origin in sorted(set(self._gateways) - wanted):
            await self._disconnect(origin)
            self._emit({"instance": origin, "type": "instance_removed", "data": {}, "seq": None})
        return sorted(self._gateways)

    async def _connect(self, origin):
        inst = self._instance_factory(origin)
        gateway = self._gateway_factory(inst)
        self._instances[origin] = inst
        self._gateways[origin] = gateway
        self._tasks[origin] = asyncio.create_task(self._pump(origin, gateway))
        self._emit({"instance": origin, "type": "instance_added", "data": {}, "seq": None})

    async def _disconnect(self, origin):
        task = self._tasks.pop(origin, None)
        gateway = self._gateways.pop(origin, None)
        self._instances.pop(origin, None)
        if task:
            task.cancel()
            with suppress(asyncio.CancelledError, Exception):
                await task
        if gateway is not None:
            with suppress(Exception):
                await gateway.close()

    async def _pump(self, origin, gateway):
        try:
            await gateway.start()
            async for event in gateway:
                self._emit({"instance": origin, **event})
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            self.errors[origin] = str(getattr(exc, "error", exc))[:100]
            self._emit({"instance": origin, "type": "instance_error", "data": {"error": self.errors[origin]}, "seq": None})

    async def _poll(self):
        while not self._closing:
            await asyncio.sleep(self.poll_interval)
            await self.refresh()

    def _emit(self, event):
        if self._events is None:
            return
        if self._events.full():
            self._events.get_nowait()
        self._events.put_nowait(event)

    async def __aenter__(self):
        return await self.start()

    async def __aexit__(self, *args):
        await self.close()

    async def close(self):
        self._closing = True
        if self._poller:
            self._poller.cancel()
            with suppress(asyncio.CancelledError):
                await self._poller
            self._poller = None
        for origin in list(self._gateways):
            await self._disconnect(origin)
        if self._events is not None:
            self._events.put_nowait(None)

    def __aiter__(self):
        return self

    async def __anext__(self):
        item = await self._events.get()
        if item is None:
            raise StopAsyncIteration
        return item

    async def run(self):
        """Dispatch events to ``on()`` callbacks (a ``"*"`` handler gets everything) until closed."""
        if self._events is None:
            await self.start()
        try:
            async for event in self:
                for fn in list(self._handlers.get(event["type"], [])) + list(self._handlers.get("*", [])):
                    result = fn(event)
                    if inspect.isawaitable(result):
                        await result
        finally:
            await self.close()

    async def send(self, origin, channel_id, content, **fields):
        """Post as the bot on one instance (``channel_id`` is the numeric id from that instance's events)."""
        inst = self.instance(origin)
        return await asyncio.to_thread(inst.bot_send, channel_id, content, **fields)
