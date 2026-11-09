"""Instance websocket clients: the user gateway (/gateway) and the bot gateway (/bot/gateway).

Both reconnect on their own with capped exponential backoff plus jitter. Consume events
with ``async for`` or register callbacks with ``on()`` and call ``run()``. There is no
event replay: after a ``gateway_ready`` that follows a reconnect, refetch what you need.
"""
from __future__ import annotations

import asyncio
import inspect
import json
import random
import uuid
from contextlib import suppress

from .client import APIError

FATAL_CLOSE_CODES = {4001: 'invalid_session', 4003: 'banned', 4004: 'authentication_failed'}


def _close_code(exc):
    received = getattr(exc, 'rcvd', None)
    if received is not None:
        return getattr(received, 'code', None)
    return getattr(exc, 'code', None)


class _Gateway:
    path = '/gateway'

    def __init__(self, instance, *, reconnect=True, min_backoff=1.0, max_backoff=30.0, timeout=30,
                 queue_size=1024, connect=None, sleep=None, jitter=None):
        self.instance = instance
        self.reconnect, self.timeout = reconnect, timeout
        self.min_backoff, self.max_backoff = min_backoff, max_backoff
        self._connect_fn, self._sleep = connect, sleep or asyncio.sleep
        self._jitter = jitter or random.random
        self._queue_size = queue_size
        self._events = None
        self._task = None
        self._socket = None
        self._handlers = {}
        self._pending = {}
        self._ready = None
        self._closing = False
        self.user = None
        self.dropped = 0

    @property
    def url(self):
        base = self.instance.url
        return ('wss' if base.startswith('https') else 'ws') + base[base.index(':'):] + self.path

    def backoff(self, attempt):
        """Delay before reconnect number ``attempt`` (0-based): 1s, 2s, 4s ... capped, with jitter."""
        capped = min(self.max_backoff, self.min_backoff * (2 ** attempt))
        return capped * (0.75 + 0.25 * self._jitter())

    def on(self, event_type, callback=None):
        """Register a callback, or use as a decorator: ``@gateway.on('chat_message')``."""
        def register(fn):
            self._handlers.setdefault(event_type, []).append(fn)
            return fn
        return register(callback) if callback else register

    async def start(self):
        if self._task:
            raise RuntimeError('Already started')
        self._closing = False
        self._events = asyncio.Queue(maxsize=self._queue_size)
        self._ready = asyncio.Event()
        self._failed = asyncio.Event()
        self._fatal = None
        self._task = asyncio.create_task(self._supervise())
        return self

    async def wait_ready(self, timeout=None):
        """Wait for the handshake; raises the APIError behind a fatal close (bad session, ban)."""
        ready = asyncio.ensure_future(self._ready.wait())
        failed = asyncio.ensure_future(self._failed.wait())
        try:
            await asyncio.wait({ready, failed}, timeout=self.timeout if timeout is None else timeout,
                               return_when=asyncio.FIRST_COMPLETED)
        finally:
            ready.cancel()
            failed.cancel()
        if self._fatal is not None:
            raise self._fatal
        if not self._ready.is_set():
            raise TimeoutError('Instance gateway did not become ready')

    async def __aenter__(self):
        await self.start()
        try:
            await self.wait_ready()
        except BaseException:
            await self.close()
            raise
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def close(self):
        self._closing = True
        if self._task:
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task
            self._task = None
        if self._socket:
            with suppress(Exception):
                await self._socket.close()
            self._socket = None
        if self._events is not None:
            self._emit(None)

    def __aiter__(self):
        return self

    async def __anext__(self):
        item = await self._events.get()
        if item is None:
            raise StopAsyncIteration
        if isinstance(item, Exception):
            raise item
        return item

    async def run(self):
        """Dispatch events to ``on()`` callbacks until closed. Starts the gateway if needed."""
        if not self._task:
            await self.start()
        try:
            async for event in self:
                for fn in list(self._handlers.get(event.get('type'), [])) + list(self._handlers.get('*', [])):
                    result = fn(event)
                    if inspect.isawaitable(result):
                        await result
        finally:
            await self.close()

    def _emit(self, event):
        if self._events.full():
            self._events.get_nowait()
            self.dropped += 1
        self._events.put_nowait(event)

    def _fail(self, exc):
        self._fatal = exc
        self._failed.set()
        self._emit(exc)
        self._emit(None)

    async def _open(self):
        if self._connect_fn:
            return await self._connect_fn(self.url)
        try:
            from websockets.asyncio.client import connect
        except ImportError:
            raise ImportError('Install nookara[realtime] to use websockets') from None
        return await connect(self.url, open_timeout=self.timeout, max_size=8 * 1024 * 1024)

    async def _supervise(self):
        attempt = 0
        try:
            while not self._closing:
                code = None
                try:
                    self._socket = await self._open()
                    await self._session(self._socket)
                except asyncio.CancelledError:
                    raise
                except APIError as exc:
                    self._fail(exc)
                    return
                except Exception as exc:
                    code = _close_code(exc)
                    if code in FATAL_CLOSE_CODES:
                        self._fail(APIError(401 if code != 4003 else 403, {'error': FATAL_CLOSE_CODES[code]}))
                        return
                finally:
                    sock, self._socket = self._socket, None
                    self._ready.clear()
                    for future in self._pending.values():
                        if not future.done():
                            future.set_exception(ConnectionError('Instance gateway closed'))
                    if sock is not None:
                        with suppress(Exception):
                            await sock.close()
                if self._authenticated_once:
                    attempt = 0
                    self._authenticated_once = False
                self._emit({'type': 'gateway_disconnected', 'code': code})
                if not self.reconnect:
                    self._emit(None)
                    return
                await self._sleep(self.backoff(attempt))
                attempt += 1
        except asyncio.CancelledError:
            raise

    _authenticated_once = False

    async def _recv(self, sock, timeout=None):
        return json.loads(await asyncio.wait_for(sock.recv(), self.timeout if timeout is None else timeout))

    async def _send(self, sock, frame):
        await sock.send(json.dumps(frame, ensure_ascii=False))


class InstanceGateway(_Gateway):
    """User gateway (protocol section 7).

    Order is fixed: ``auth`` first, wait for ``auth_success``, then ``chat_hello``, and
    ``gateway_ready`` is emitted once the server answers ``chat_ready``. Ping every 25 s.
    """
    path = '/gateway'
    ping_interval = 25.0

    async def _session(self, sock):
        await self._send(sock, {'type': 'auth', 'session': self.instance.session})
        while True:
            frame = await self._recv(sock)
            if frame.get('type') == 'auth_success':
                self.user = frame.get('user')
                break
            if frame.get('type') in ('auth_error', 'error'):
                raise APIError(401, frame)
            self._emit(frame)
        self._authenticated_once = True
        await self._send(sock, {'type': 'chat_hello'})
        pinger = asyncio.create_task(self._ping(sock))
        try:
            self._emit(frame)
            while True:
                frame = await self._recv(sock, timeout=self.ping_interval * 3)
                kind = frame.get('type')
                if kind == 'pong':
                    continue
                if kind == 'chat_ready':
                    self._ready.set()
                    self._emit({**frame, 'type': 'gateway_ready'})
                    continue
                future = self._pending.get(frame.get('nonce'))
                if future and not future.done() and kind in ('chat_ack', 'chat_error'):
                    if kind == 'chat_error':
                        future.set_exception(APIError(400, frame))
                    else:
                        future.set_result(frame)
                    continue
                self._emit(frame)
        finally:
            pinger.cancel()
            with suppress(asyncio.CancelledError):
                await pinger

    async def _ping(self, sock):
        while True:
            await asyncio.sleep(self.ping_interval)
            await self._send(sock, {'type': 'ping'})

    async def send(self, event_type, **fields):
        if not self._socket or not self._ready.is_set():
            raise ConnectionError('Instance gateway is not ready')
        await self._send(self._socket, {**fields, 'type': event_type})

    async def rpc(self, event_type, *, timeout=None, **fields):
        nonce = uuid.uuid4().hex
        future = asyncio.get_running_loop().create_future()
        self._pending[nonce] = future
        try:
            await self.send(event_type, **{**fields, 'nonce': nonce})
            return await asyncio.wait_for(future, self.timeout if timeout is None else timeout)
        finally:
            self._pending.pop(nonce, None)

    async def send_message(self, channel, message, *, reply_to=None, attachments=None, sign=None, alias=None, sticker=None):
        """chat_send with the server's ``chat_ack`` as the result (signed when signing is enabled). ``alias`` is for bots only.
        ``sticker=<tid>`` sends one of the server's stickers (the message may be empty)."""
        fields = {'channel': channel, 'message': message}
        if sticker is not None:
            fields['sticker'] = sticker
        if alias is not None:
            from .instance import make_alias
            fields['alias'] = make_alias(alias)
        if reply_to is not None:
            fields['reply_to'] = reply_to
        if attachments:
            fields['attachments'] = attachments
        signature = self.instance._signature(sign, channel, message, attachments=attachments or (), reply_to=reply_to)
        if signature is not None:
            fields['signature'] = signature
        return (await self.rpc('chat_send', **fields))['message']

    async def typing(self, channel, typing=True):
        await self.send('chat_typing', channel=channel, typing=typing)

    async def mark_read(self, channel, message_id):
        await self.send('chat_read', channel=channel, message_id=message_id)


class BotGateway(_Gateway):
    """Bot gateway (section 14), Discord-style opcodes. Events arrive as ``{type, data, seq}``."""
    path = '/bot/gateway'

    async def _session(self, sock):
        hello = await self._recv(sock)
        if hello.get('op') != 10:
            raise APIError(400, {'error': 'unexpected_hello'})
        interval = hello['d']['heartbeat_interval'] / 1000
        await self._send(sock, {'op': 2, 'd': {'token': self.instance.bot_token}})
        beat = asyncio.create_task(self._heartbeat(sock, interval))
        try:
            while True:
                frame = await self._recv(sock, timeout=interval * 3)
                if frame.get('op') == 0:
                    if frame.get('t') == 'READY':
                        self._authenticated_once = True
                        self.user = frame['d'].get('user')
                        self._ready.set()
                        self._emit({'type': 'gateway_ready', 'data': frame['d']})
                    else:
                        self._emit({'type': frame['t'], 'data': frame['d'], 'seq': frame.get('s')})
        finally:
            beat.cancel()
            with suppress(asyncio.CancelledError):
                await beat

    async def _heartbeat(self, sock, interval):
        while True:
            await asyncio.sleep(interval)
            await self._send(sock, {'op': 1, 'd': None})
