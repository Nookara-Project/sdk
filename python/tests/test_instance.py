import asyncio
import base64
import json
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

project_root = Path(__file__).parents[1]
sys.path.insert(0, str(project_root / 'python' if (project_root / 'python').is_dir() else project_root))
from velora_api import APIError, BotGateway, Client, Instance, InstanceGateway, Signer, execute_webhook, normalize_origin
from velora_api import signing
from velora_api.instance import INSTANCE_OPERATIONS, parse_webhook_url

VELORA_TOKEN = 'velora-secret-token'
SESSION = 'instance-session-token'


class Handler(BaseHTTPRequestHandler):
    seen = []

    def log_message(self, *args):
        pass

    def do_GET(self):
        self.handle_request()
    do_POST = do_PUT = do_PATCH = do_DELETE = do_GET

    def handle_request(self):
        content = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        type(self).seen.append((self.command, self.path, dict(self.headers), content))
        if self.path.startswith('/api/v1/auth/'):
            body = {'session': SESSION, 'user': {'id': 'v:7', 'kind': 'velora', 'velora_id': '7', 'username': 'nat'}}
        elif self.path == '/.well-known/bonfire':
            body = {'software': 'bonfire-server', 'name': 'Test', 'accounts_mode': 'velora', 'features': {'signing': True}, 'build': {'version': '0.1.0'}, 'read_only': False, 'community': {'sid': 'sCOMM'}}
        elif self.path == '/api/v1/instance/backups' and self.command == 'POST':
            body = {'backup': {'id': 'b1'}}
        elif self.path.split('?')[0].endswith('/webhooks/w1/tok'):
            self.send_response(204)
            self.end_headers()
            return
        else:
            body = {'ok': True}
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())


class InstanceRestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        Handler.seen.clear()

    def instance(self, **kw):
        return Instance(self.base + '/some/path?x=1', allow_insecure=True, **kw)

    def test_url_normalization(self):
        self.assertEqual(normalize_origin('HTTPS://Chat.Ikelene.NET:443/a/b?c#d'), 'https://chat.ikelene.net')
        self.assertEqual(normalize_origin('https://example.com:8443/'), 'https://example.com:8443')
        self.assertEqual(normalize_origin('http://localhost:80', allow_insecure=True), 'http://localhost')
        self.assertEqual(normalize_origin('https://bücher.example'), 'https://xn--bcher-kva.example')
        for bad in ['http://example.com', 'ftp://example.com', 'https://user:pw@example.com', 'example.com', 'https://']:
            with self.assertRaises(ValueError):
                normalize_origin(bad)
        self.assertEqual(self.instance().url, self.base)

    def test_velora_token_never_reaches_instance(self):
        velora = Client(VELORA_TOKEN, base_url='http://127.0.0.1:1', allow_insecure=True)
        with patch.object(velora, 'post_bonfire_instance_token', return_value={'token': 'ticket.jwt.sig'}) as mint:
            inst = self.instance()
            result = inst.login_with_velora(velora)
        mint.assert_called_once_with(json={'instance': self.base})
        self.assertEqual(result['session'], SESSION)
        method, path, headers, body = Handler.seen[-1]
        self.assertEqual((method, path), ('POST', '/api/v1/auth/velora'))
        self.assertNotIn('Authorization', headers)
        self.assertEqual(json.loads(body), {'token': 'ticket.jwt.sig'})
        for _, _, h, b in Handler.seen:
            self.assertNotIn(VELORA_TOKEN.encode(), b)
            self.assertNotIn(VELORA_TOKEN, json.dumps(h))
        self.assertEqual(inst.session, SESSION)
        self.assertNotIn(SESSION, repr(inst))
        with self.assertRaises(TypeError):
            inst.login_with_velora(inst)

    def test_local_account_flows_and_logout(self):
        inst = self.instance()
        inst.register('nat', 'password123')
        self.assertEqual(Handler.seen[-1][1], '/api/v1/auth/register')
        self.assertEqual(json.loads(Handler.seen[-1][3]), {'username': 'nat', 'password': 'password123'})
        inst.login('nat', 'password123')
        self.assertEqual(Handler.seen[-1][1], '/api/v1/auth/login')
        self.assertNotIn('Authorization', Handler.seen[-1][2])
        inst.get_api_v1_me()
        self.assertEqual(Handler.seen[-1][2]['Authorization'], 'Bearer ' + SESSION)
        inst.logout()
        self.assertEqual(Handler.seen[-1][1], '/api/v1/auth/logout')
        self.assertIsNone(inst.session)
        self.assertIsNone(inst.user)

    def test_session_and_bot_token_are_exclusive(self):
        with self.assertRaises(ValueError):
            Instance(self.base, 's', bot_token='b', allow_insecure=True)
        bot = Instance(self.base, bot_token='bot-secret', allow_insecure=True)
        bot.get_bot_v1_users_me()
        self.assertEqual(Handler.seen[-1][2]['Authorization'], 'Bot bot-secret')
        with self.assertRaises(ValueError):
            bot.get_api_v1_me()
        with self.assertRaises(ValueError):
            self.instance().bot_gateway()

    def test_rest_helpers_dispatch(self):
        inst = Instance(self.base, SESSION, allow_insecure=True)
        self.assertEqual(inst.channel_id.__name__, 'channel_id')
        with patch.object(inst, 'get_api_v1_servers_by_sid', return_value={'channels': [{'cid': 'c1', 'name': 'General'}, {'cid': 'c2', 'name': 'bots'}]}):
            self.assertEqual(inst.channel_id('#general'), 'c1')
            self.assertEqual(inst.channel_id('c2'), 'c2')
            with self.assertRaises(LookupError):
                inst.channel_id('missing')
        inst.send_message('c1', 'hi', reply_to='5')
        method, path, _, body = Handler.seen[-1]
        self.assertEqual((method, path), ('POST', '/api/v1/channels/c1/messages'))
        self.assertEqual(json.loads(body), {'message': 'hi', 'reply_to': '5', 'attachments': []})
        inst.edit_message('9', 'new')
        self.assertEqual(Handler.seen[-1][:2], ('PATCH', '/api/v1/messages/9'))
        inst.react('9', '\U0001f44d')
        self.assertEqual(Handler.seen[-1][:2], ('PUT', '/api/v1/messages/9/reactions/%F0%9F%91%8D'))
        inst.delete_message('9')
        self.assertEqual(Handler.seen[-1][:2], ('DELETE', '/api/v1/messages/9'))
        inst.pin('9')
        self.assertEqual(Handler.seen[-1][:2], ('PUT', '/api/v1/messages/9/pin'))
        inst.messages('c1', limit=5)
        self.assertEqual(Handler.seen[-1][1], '/api/v1/channels/c1/messages?limit=5')
        inst.search('c1', 'a b')
        self.assertEqual(Handler.seen[-1][1], '/api/v1/channels/c1/search?q=a+b')
        inst.members()
        self.assertEqual(Handler.seen[-1][1], '/api/v1/servers/sCOMM/members')
        inst.create_webhook('c1', 'Scores')
        self.assertEqual(json.loads(Handler.seen[-1][3]), {'name': 'Scores'})
        inst.create_backup('before update')
        self.assertEqual(Handler.seen[-1][:2], ('POST', '/api/v1/instance/backups'))
        inst.update_settings(registration='closed')
        self.assertEqual(json.loads(Handler.seen[-1][3]), {'registration': 'closed'})
        bot = Instance(self.base, bot_token='b', allow_insecure=True)
        bot.bot_send('12', 'pong')
        self.assertEqual(Handler.seen[-1][:2], ('POST', '/bot/v1/channels/12/messages'))
        self.assertEqual(json.loads(Handler.seen[-1][3]), {'content': 'pong'})
        bot.bot_send('12', 'hi', alias={'name': 'Narrator', 'avatar_url': 'https://example.com/n.png'})
        self.assertEqual(json.loads(Handler.seen[-1][3]), {'content': 'hi', 'alias': {'name': 'Narrator', 'avatar_url': 'https://example.com/n.png'}})
        bot.bot_edit('12', '34', alias=None)
        self.assertEqual(Handler.seen[-1][:2], ('PATCH', '/bot/v1/channels/12/messages/34'))
        self.assertEqual(json.loads(Handler.seen[-1][3]), {'alias': None})
        bot.bot_edit('12', '34', 'x', alias={'name': 'B'})
        self.assertEqual(json.loads(Handler.seen[-1][3]), {'content': 'x', 'alias': {'name': 'B'}})
        for bad in ({'name': ''}, {'name': 'a' * 33}, {'name': 'a\nb'}, {'name': 'ok', 'avatar_url': 'http://x/y.png'}, {'name': 'ok', 'avatar_url': 'https://u:p@x/y.png'}, {'name': 'ok', 'avatar_url': 'https://x/a b.png'}, {'name': 'ok', 'avatar_url': 'https://x/' + 'a' * 500}):
            with self.assertRaises(ValueError):
                bot.bot_send('12', 'no', alias=bad)
        with self.assertRaises(ValueError):
            bot.bot_edit('12', '34')

    def test_all_instance_operations(self):
        for op, route in INSTANCE_OPERATIONS.items():
            inst = Instance(self.base, bot_token='b', allow_insecure=True) if route['auth'] == 'bot' else Instance(self.base, 's', allow_insecure=True)
            params = {p['name']: 'v /x' for p in route['params']}
            with patch.object(inst, 'request', return_value='ok') as request:
                self.assertEqual(getattr(inst, op)(**params), 'ok')
                args, kw = request.call_args
                self.assertEqual(args[0], route['method'])
                self.assertNotIn(':', args[1].split('?')[0].replace('/.well-known', '').replace('@me', ''))
                self.assertEqual(kw['auth'], route['auth'] != 'none')
        self.assertGreaterEqual(len(INSTANCE_OPERATIONS), 140)

    def test_webhook_execute_without_login(self):
        inst = self.instance()
        self.assertIsNone(inst.execute_webhook('w1', 'tok', 'Score: 10'))
        method, path, headers, body = Handler.seen[-1]
        self.assertEqual((method, path), ('POST', '/api/v1/webhooks/w1/tok?wait=false'))
        self.assertNotIn('Authorization', headers)
        self.assertEqual(json.loads(body), {'content': 'Score: 10'})
        self.assertEqual(parse_webhook_url('https://chat.ikelene.net/api/v1/webhooks/abc/def'), ('https://chat.ikelene.net', 'abc', 'def'))
        for bad in ['https://chat.ikelene.net/api/v1/webhooks/abc', 'https://chat.ikelene.net/x/abc/def', 'https://chat.ikelene.net/api/v1/webhooks/a/b?x=1']:
            with self.assertRaises(ValueError):
                parse_webhook_url(bad)
        execute_webhook(self.base + '/api/v1/webhooks/w1/tok', 'Hi', username='Bot', allow_insecure=True)
        self.assertEqual(json.loads(Handler.seen[-1][3]), {'content': 'Hi', 'username': 'Bot'})
        inst.execute_webhook('w1', 'tok', 'with file', files={'files[0]': ('a.txt', b'abc', 'text/plain')})
        self.assertIn(b'payload_json', Handler.seen[-1][3])


class SigningTests(unittest.TestCase):
    def setUp(self):
        try:
            from cryptography.hazmat.primitives import serialization
            from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
        except ImportError:
            self.skipTest('cryptography not installed')
        self.private = Ed25519PrivateKey.generate()
        der = self.private.private_bytes(serialization.Encoding.DER, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
        self.key_response = {'kid': 'k_abc', 'public_key': 'x', 'private_key': signing.b64url(der)}

    def test_canonical_json_and_signing_bytes(self):
        self.assertEqual(signing.canonical({'b': 1, 'a': [True, None, 'é', 2.0], 'c': {'z': 1, 'y': 'x'}}),
                         '{"a":[true,null,"é",2],"b":1,"c":{"y":"x","z":1}}')
        payload = signing.build_payload(iss='https://velora.ikelene.net', instance='https://chat.ikelene.net', community='s1', channel='c1',
                                        author=7, ts=1760000000000, nonce='n', body='a\r\nb', attachments=['ab'], reply_to=5)
        self.assertEqual(payload['body'], 'a\nb')
        self.assertEqual(payload['author'], '7')
        self.assertEqual(payload['reply_to'], '5')
        self.assertIsNone(payload['edit_of'])
        text = signing.signing_bytes(payload).decode()
        self.assertTrue(text.startswith('bonfire-msg-v1\n{"attachments":["ab"],"author":"7","body":"a\\nb","channel":"c1","community":"s1"'))
        self.assertIn('"edit_of":null', text)
        self.assertTrue(text.endswith('"ts":1760000000000,"v":1}'))

    def test_signature_verifies(self):
        signer = Signer.from_key_response(self.key_response, iss='https://velora.ikelene.net')
        self.assertNotIn(self.key_response['private_key'], repr(signer))
        sig = signer.sign(instance='https://chat.ikelene.net', community='s1', channel='c1', author='7', body='hello', ts=1760000000000, nonce='nn')
        self.assertEqual(set(sig), {'kid', 'sig', 'ts', 'nonce'})
        self.assertEqual((sig['kid'], sig['ts'], sig['nonce']), ('k_abc', 1760000000000, 'nn'))
        raw = base64.urlsafe_b64decode(sig['sig'] + '==')
        self.assertEqual(len(raw), 64)
        payload = signing.build_payload(iss='https://velora.ikelene.net', instance='https://chat.ikelene.net', community='s1', channel='c1',
                                        author='7', ts=1760000000000, nonce='nn', body='hello')
        self.private.public_key().verify(raw, signing.signing_bytes(payload))

    def test_instance_signs_automatically(self):
        inst = Instance('https://chat.ikelene.net', 'sess')
        inst.user = {'id': 'v:7', 'velora_id': '7'}
        inst._community = 'sCOMM'
        inst.signer = Signer.from_key_response(self.key_response, iss='https://velora.ikelene.net')
        sent = []
        with patch.object(inst, 'post_api_v1_channels_by_cid_messages', side_effect=lambda **kw: sent.append(kw)):
            inst.send_message('c1', 'signed')
            inst.send_message('c1', 'plain', sign=False)
        self.assertEqual(set(sent[0]['json']['signature']), {'kid', 'sig', 'ts', 'nonce'})
        self.assertNotIn('signature', sent[1]['json'])
        with patch.object(inst, 'patch_api_v1_messages_by_id', side_effect=lambda **kw: sent.append(kw)):
            with self.assertRaises(ValueError):
                inst.edit_message('9', 'x')
            inst.edit_message('9', 'edited', channel='c1')
        self.assertIn('signature', sent[2]['json'])

    def test_enable_signing_fetches_key_from_velora_only(self):
        velora = Client(VELORA_TOKEN, base_url='https://velora.ikelene.net')
        inst = Instance('https://chat.ikelene.net')
        inst.info = {'software': 'bonfire-server', 'velora': {'issuer': 'https://velora.ikelene.net/'}}
        with patch.object(velora, 'get_bonfire_signing_key', return_value=self.key_response) as get:
            signer = inst.enable_signing(velora)
        get.assert_called_once_with()
        self.assertEqual(signer.iss, 'https://velora.ikelene.net')
        via_new = Client(VELORA_TOKEN, base_url='https://nookara.cc')
        with patch.object(via_new, 'get_bonfire_signing_key', return_value=self.key_response):
            self.assertEqual(inst.enable_signing(via_new).iss, 'https://velora.ikelene.net')
        bare = Instance('https://chat.ikelene.net')
        bare.info = {'software': 'bonfire-server'}
        with patch.object(via_new, 'get_bonfire_signing_key', return_value=self.key_response):
            self.assertEqual(bare.enable_signing(via_new).iss, 'https://velora.ikelene.net')
        plain = Instance('https://chat.ikelene.net', 'sess')
        with self.assertRaises(ValueError):
            plain._signature(True, 'c1', 'x')
        self.assertIsNone(plain._signature(None, 'c1', 'x'))


class VeloraSideTests(unittest.TestCase):
    def test_instance_list_sync_and_hosting_payloads(self):
        c = Client('t')
        with patch.object(c, 'get_bonfire_instances', return_value={'instances': [{'url': 'https://a.example'}]}), \
                patch.object(c, 'put_bonfire_instances', return_value={'instances': []}) as put:
            c.sync_bonfire_instances(['https://B.example:443/x', 'https://a.example'])
        self.assertEqual(put.call_args.kwargs['json'], {'instances': [{'url': 'https://a.example'}, {'url': 'https://b.example'}]})
        with patch.object(c, 'post_bonfire_hosting_servers', return_value={}) as post:
            c.create_hosting_server('camp', 'Camp', 'plus', weeks=2)
        self.assertEqual(post.call_args.kwargs['json'], {'slug': 'camp', 'name': 'Camp', 'plan': 'plus', 'weeks': 2})
        with patch.object(c, 'delete_bonfire_hosting_servers_by_slug', return_value={}) as delete:
            c.delete_hosting_server('camp')
        self.assertEqual(delete.call_args.kwargs, {'slug': 'camp', 'json': {'confirm': 'camp'}})
        with patch.object(c, 'get_bonfire_directory', return_value={}) as directory:
            c.bonfire_directory('game')
        self.assertEqual(directory.call_args.kwargs['query'], {'q': 'game', 'page': None})


class FakeClosed(Exception):
    def __init__(self, code):
        super().__init__(code)
        self.code = code


class FakeSocket:
    """Scripted websocket: the script is a list of frames to send; strings starting
    with 'close:' raise a close with that code once the server side runs out."""

    def __init__(self, script, log):
        self.script, self.log, self.incoming = list(script), log, asyncio.Queue()
        self.closed = False

    async def send(self, raw):
        frame = json.loads(raw)
        self.log.append(frame)
        await self.incoming.put(frame)

    async def recv(self):
        while True:
            if self.script:
                step = self.script[0]
                if callable(step):
                    produced = step(self.log)
                    if produced is None:
                        await asyncio.sleep(0.005)
                        continue
                    self.script.pop(0)
                    if isinstance(produced, int):
                        raise FakeClosed(produced)
                    return json.dumps(produced)
                self.script.pop(0)
                if isinstance(step, int):
                    raise FakeClosed(step)
                return json.dumps(step)
            await asyncio.sleep(3600)

    async def close(self):
        self.closed = True


def when_sent(kind, reply):
    def step(log):
        for frame in log:
            if frame.get('type') == kind or frame.get('op') == kind:
                return reply(frame) if callable(reply) else reply
        return None
    return step


class GatewayTests(unittest.IsolatedAsyncioTestCase):
    def inst(self):
        return Instance('https://chat.ikelene.net', 'sess')

    async def test_auth_ordering_ack_and_pong(self):
        log = []
        script = [
            when_sent('auth', {'type': 'auth_success', 'user': {'id': 'v:7'}}),
            when_sent('chat_hello', {'type': 'chat_ready'}),
            {'type': 'chat_message', 'message': {'body': 'hi'}},
            when_sent('chat_send', lambda f: {'type': 'chat_ack', 'nonce': f['nonce'], 'message': {'body': f['message']}}),
            {'type': 'pong'},
            {'type': 'chat_message', 'message': {'body': 'bye'}},
        ]
        gateway = self.inst().gateway(connect=lambda url: self._open(url, script, log))
        async with gateway:
            self.assertEqual(gateway.url, 'wss://chat.ikelene.net/gateway')
            self.assertEqual([f['type'] for f in log], ['auth', 'chat_hello'])
            self.assertEqual(log[0], {'type': 'auth', 'session': 'sess'})
            types = []
            async for event in gateway:
                types.append(event['type'])
                if event['type'] == 'gateway_ready':
                    ack = await gateway.send_message('c1', 'hello')
                    self.assertEqual(ack, {'body': 'hello'})
                if len([t for t in types if t == 'chat_message']) == 2:
                    break
        self.assertEqual(log[2]['type'], 'chat_send')
        self.assertEqual((log[2]['channel'], log[2]['message']), ('c1', 'hello'))
        self.assertIn('nonce', log[2])
        self.assertEqual(types[:2], ['auth_success', 'gateway_ready'])
        self.assertNotIn('pong', types)

    async def _open(self, url, script, log):
        self.opened = getattr(self, 'opened', []) + [url]
        return FakeSocket(script, log)

    async def test_callbacks_and_run(self):
        log = []
        script = [when_sent('auth', {'type': 'auth_success'}), when_sent('chat_hello', {'type': 'chat_ready'}),
                  {'type': 'chat_message', 'message': {'body': '!ping'}}]
        gateway = self.inst().gateway(connect=lambda url: self._open(url, script, log))
        seen = []

        @gateway.on('chat_message')
        async def handle(event):
            seen.append(event['message']['body'])
            await gateway.close()

        await asyncio.wait_for(gateway.run(), 2)
        self.assertEqual(seen, ['!ping'])

    async def test_reconnect_with_capped_backoff_and_resend_auth(self):
        sleeps = []

        async def sleep(delay):
            sleeps.append(delay)

        logs = [[], [], []]
        scripts = [
            [when_sent('auth', {'type': 'auth_success'}), 4010],
            [1006],
            [when_sent('auth', {'type': 'auth_success'}), when_sent('chat_hello', {'type': 'chat_ready'}), {'type': 'chat_message', 'message': {'body': 'back'}}],
        ]
        sockets = iter(zip(scripts, logs))

        async def connect(url):
            script, log = next(sockets)
            return FakeSocket(script, log)

        gateway = self.inst().gateway(connect=connect, sleep=sleep, jitter=lambda: 1.0)
        got = []
        async with gateway:
            async for event in gateway:
                got.append(event['type'])
                if event['type'] == 'chat_message':
                    break
        self.assertEqual(got.count('gateway_disconnected'), 2)
        self.assertEqual(sleeps, [1.0, 2.0])
        for log in logs:
            self.assertEqual(log[0], {'type': 'auth', 'session': 'sess'})
        self.assertEqual([f['type'] for f in logs[2]], ['auth', 'chat_hello'])

    async def test_backoff_cap_and_jitter_bounds(self):
        gateway = self.inst().gateway(jitter=lambda: 0.0)
        self.assertEqual([gateway.backoff(n) for n in (0, 1, 2)], [0.75, 1.5, 3.0])
        self.assertEqual(gateway.backoff(20), 30 * 0.75)
        gateway = self.inst().gateway(jitter=lambda: 0.999)
        self.assertLessEqual(gateway.backoff(20), 30.0)
        self.assertGreaterEqual(self.inst().gateway().backoff(0), 0.75)

    async def test_invalid_session_is_fatal(self):
        log = []
        gateway = self.inst().gateway(connect=lambda url: self._open(url, [when_sent('auth', 4001)], log), sleep=lambda d: asyncio.sleep(0))
        with self.assertRaises(APIError) as ctx:
            async with gateway:
                pass
        self.assertEqual(ctx.exception.error, 'invalid_session')
        self.assertEqual(ctx.exception.status, 401)

    async def test_ping_frames(self):
        log = []
        gateway = InstanceGateway(self.inst(), connect=lambda url: self._open(url, [when_sent('auth', {'type': 'auth_success'}), when_sent('chat_hello', {'type': 'chat_ready'})], log))
        gateway.ping_interval = 0.02
        async with gateway:
            await asyncio.sleep(0.1)
        self.assertGreaterEqual([f['type'] for f in log].count('ping'), 2)

    async def test_send_requires_ready(self):
        gateway = self.inst().gateway()
        with self.assertRaises(ConnectionError):
            await gateway.send('chat_typing', channel='c1')

    async def test_bot_gateway_handshake_and_events(self):
        log = []
        bot = Instance('https://chat.ikelene.net', bot_token='bot-tok')
        script = [{'op': 10, 'd': {'heartbeat_interval': 40}}, when_sent(2, {'op': 0, 't': 'READY', 's': 1, 'd': {'user': {'id': '3'}}}),
                  {'op': 0, 't': 'MESSAGE_CREATE', 's': 2, 'd': {'content': '!ping', 'channel_id': '5'}}]
        gateway = bot.bot_gateway(connect=lambda url: self._open(url, script, log))
        events = []
        async with gateway:
            self.assertEqual(gateway.url, 'wss://chat.ikelene.net/bot/gateway')
            async for event in gateway:
                events.append(event)
                if event['type'] == 'MESSAGE_CREATE':
                    break
            await asyncio.sleep(0.12)
        self.assertEqual(log[0], {'op': 2, 'd': {'token': 'bot-tok'}})
        self.assertEqual(events[-1]['data']['content'], '!ping')
        self.assertTrue(any(f.get('op') == 1 for f in log[1:]))
        self.assertIsInstance(gateway, BotGateway)


if __name__ == '__main__':
    unittest.main()
