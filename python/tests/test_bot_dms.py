"""Bot DMs of 0.9.8: BotClient DM helpers, DMRefused, plain Client.send_dm to bots, DM gateway events."""
import asyncio
import json
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

project_root = Path(__file__).parents[1]
sys.path.insert(0, str(project_root / 'python' if (project_root / 'python').is_dir() else project_root))
sys.path.insert(0, str(Path(__file__).parent))
from nookara import APIError, BotClient, BotGateway, Client, DMRefused, dm_channel_id, dm_user_id, is_dm_event
from test_instance import FakeSocket, when_sent


class Handler(BaseHTTPRequestHandler):
    seen = []
    replies = []

    def log_message(self, *args):
        pass

    def handle_any(self):
        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length)
        type(self).seen.append((self.command, self.path, dict(self.headers), json.loads(raw) if raw else None))
        status, body = type(self).replies.pop(0) if type(self).replies else (200, {})
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())
    do_GET = do_POST = do_PATCH = do_DELETE = handle_any


class BotDMHttpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.base = 'http://127.0.0.1:%d' % cls.server.server_port

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        Handler.seen, Handler.replies = [], []
        self.bot = BotClient('BOTTOKEN', base_url=self.base, allow_insecure=True)

    def test_open_dm_by_id_and_username(self):
        Handler.replies = [(200, {'id': '1000000000012', 'type': 1}), (200, {'id': '1000000000012', 'type': 1})]
        self.assertEqual(self.bot.open_dm(user_id=12)['id'], '1000000000012')
        self.bot.open_dm(username='@alice')
        first, second = Handler.seen
        self.assertEqual((first[0], first[1], first[3]), ('POST', '/chat/api/v1/users/@me/channels', {'recipient_id': '12'}))
        self.assertEqual(first[2]['Authorization'], 'Bot BOTTOKEN')
        self.assertEqual(second[3], {'username': 'alice'})

    def test_open_dm_needs_exactly_one_target(self):
        with self.assertRaises(ValueError):
            self.bot.open_dm()
        with self.assertRaises(ValueError):
            self.bot.open_dm(user_id=1, username='a')

    def test_refusals_become_dm_refused(self):
        for code in ('bot_no_shared_server', 'dm_privacy', 'bot_dms_off', 'cannot_dm_bot', 'user_blocked'):
            Handler.replies = [(403, {'message': 'Cannot send messages to this user', 'code': 50007, 'error': code, 'detail': 'words'})]
            with self.assertRaises(DMRefused) as ctx:
                self.bot.open_dm(username='alice')
            self.assertEqual((ctx.exception.error, ctx.exception.detail, ctx.exception.status), (code, 'words', 403))
            self.assertIsInstance(ctx.exception, APIError)

    def test_other_errors_stay_api_errors(self):
        Handler.replies = [(404, {'message': 'user_not_found', 'code': 0, 'error': 'user_not_found'}),
                           (429, {'message': 'You are being rate limited.', 'code': 0, 'error': 'rate_limited', 'retry_after': 7})]
        with self.assertRaises(APIError) as ctx:
            self.bot.open_dm(username='nobody')
        self.assertNotIsInstance(ctx.exception, DMRefused)
        with self.assertRaises(APIError) as ctx:
            self.bot.send_dm_message('1000000000012', 'hi')
        self.assertEqual((ctx.exception.status, ctx.exception.retry_after), (429, 7.0))

    def test_send_history_edit_delete_typing(self):
        cid = '1000000000012'
        Handler.replies = [(200, {'id': '5'})] * 7
        self.bot.send_dm_message(cid, 'hello <@12>', reply_to=3)
        self.bot.dm_history(cid, before=9, limit=10)
        self.bot.dm_message(cid, 5)
        self.bot.edit_dm_message(cid, 5, 'edited')
        self.bot.delete_dm_message(cid, 5)
        self.bot.dm_typing(cid)
        self.bot.dm_channel(cid)
        paths = [(m, p) for m, p, _, _ in Handler.seen]
        self.assertEqual(paths, [
            ('POST', '/chat/api/v1/channels/1000000000012/messages'),
            ('GET', '/chat/api/v1/channels/1000000000012/messages?before=9&limit=10'),
            ('GET', '/chat/api/v1/channels/1000000000012/messages/5'),
            ('PATCH', '/chat/api/v1/channels/1000000000012/messages/5'),
            ('DELETE', '/chat/api/v1/channels/1000000000012/messages/5'),
            ('POST', '/chat/api/v1/channels/1000000000012/typing'),
            ('GET', '/chat/api/v1/channels/1000000000012'),
        ])
        self.assertEqual(Handler.seen[0][3], {'content': 'hello <@12>', 'message_reference': {'message_id': '3'}})
        self.assertEqual(Handler.seen[3][3], {'content': 'edited'})

    def test_bad_ids_rejected_before_any_request(self):
        for bad in ('../x', '', 'abc', '1/2'):
            with self.assertRaises(ValueError):
                self.bot.send_dm_message(bad, 'x')
        self.assertEqual(Handler.seen, [])

    def test_user_send_dm_is_plain_to_bots(self):
        Handler.replies = [(200, {'success': True, 'sent': ['mybot']})]
        me = Client('USERTOKEN', base_url=self.base, allow_insecure=True)
        me.send_dm('mybot', 'hello', reply_to=4)
        method, path, headers, body = Handler.seen[0]
        self.assertEqual((method, path, body), ('POST', '/im/send', {'to': 'mybot', 'message': 'hello', 'reply_to': 4}))
        self.assertEqual(headers['Authorization'], 'Bearer USERTOKEN')
        self.assertNotIn('enc', body)

    def test_user_send_dm_to_person_still_points_at_e2ee(self):
        Handler.replies = [(400, {'error': 'e2ee_required', 'message': 'locked'})]
        me = Client('USERTOKEN', base_url=self.base, allow_insecure=True)
        with self.assertRaisesRegex(RuntimeError, 'EncryptedDMs'):
            me.send_dm('alice', 'hello')

    def test_user_send_dm_other_errors_pass_through(self):
        Handler.replies = [(403, {'error': 'user_blocked'})]
        me = Client('USERTOKEN', base_url=self.base, allow_insecure=True)
        with self.assertRaises(APIError) as ctx:
            me.send_dm('mybot', 'hello')
        self.assertEqual(ctx.exception.error, 'user_blocked')

    def test_bot_account(self):
        Handler.replies = [(200, {'id': '9', 'username': 'mybot', 'pfp': None, 'dm': True})]
        me = Client('USERTOKEN', base_url=self.base, allow_insecure=True)
        self.assertEqual(me.bot_account(9)['username'], 'mybot')
        self.assertEqual(Handler.seen[0][1], '/chat/bots/by-id/9')


class HelperTests(unittest.TestCase):
    def test_channel_ids(self):
        self.assertEqual(dm_channel_id(12), '1000000000012')
        self.assertEqual(dm_user_id('1000000000012'), '12')
        self.assertIsNone(dm_user_id('55'))
        self.assertIsNone(dm_user_id('abc'))

    def test_is_dm_event(self):
        dm = {'type': 'MESSAGE_CREATE', 'data': {'id': '1', 'channel_id': '1000000000012', 'bonfire': {'dm': True, 'with': 'alice'}}}
        guild = {'type': 'MESSAGE_CREATE', 'data': {'id': '1', 'guild_id': '4', 'channel_id': '7'}}
        other = {'type': 'GUILD_CREATE', 'data': {'bonfire': {'dm': True}}}
        self.assertTrue(is_dm_event(dm))
        self.assertTrue(is_dm_event(dm['data']))
        self.assertFalse(is_dm_event(guild))
        self.assertFalse(is_dm_event(other))
        self.assertFalse(is_dm_event(None))


class BotGatewayDMTests(unittest.IsolatedAsyncioTestCase):
    async def test_nookara_gateway_url_and_dm_flag(self):
        log, opened = [], []
        dm = {'id': '8', 'channel_id': '1000000000012', 'content': 'hi bot', 'author': {'id': '12'}, 'bonfire': {'dm': True, 'with': 'alice'}}
        script = [{'op': 10, 'd': {'heartbeat_interval': 40000}},
                  when_sent(2, {'op': 0, 't': 'READY', 's': 1, 'd': {'user': {'id': '3'}}}),
                  {'op': 0, 't': 'MESSAGE_CREATE', 's': 2, 'd': {'id': '1', 'guild_id': '4', 'channel_id': '7', 'content': 'in a server'}},
                  {'op': 0, 't': 'MESSAGE_CREATE', 's': 3, 'd': dm}]

        async def connect(url):
            opened.append(url)
            return FakeSocket(script, log)
        bot = BotClient('BOTTOKEN')
        gateway = bot.gateway(connect=connect)
        self.assertIsInstance(gateway, BotGateway)
        events = []
        async with gateway:
            async for event in gateway:
                events.append(event)
                if len([e for e in events if e['type'] == 'MESSAGE_CREATE']) == 2:
                    break
        self.assertEqual(opened, ['wss://nookara.cc/chat/gateway'])
        self.assertEqual(log[0], {'op': 2, 'd': {'token': 'BOTTOKEN'}})
        messages = [e for e in events if e['type'] == 'MESSAGE_CREATE']
        self.assertEqual([e['dm'] for e in messages], [False, True])
        self.assertEqual([is_dm_event(e) for e in messages], [False, True])
        self.assertEqual(gateway.user, {'id': '3'})

    async def test_instance_gateway_path_default_unchanged(self):
        from nookara import Instance
        gateway = Instance('https://chat.ikelene.net', bot_token='t').bot_gateway()
        self.assertEqual(gateway.url, 'wss://chat.ikelene.net/bot/gateway')


if __name__ == '__main__':
    unittest.main()
