"""Personal emojis (Nookara) and server stickers (Ember instances)."""
import json
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

project_root = Path(__file__).parents[1]
sys.path.insert(0, str(project_root / 'python' if (project_root / 'python').is_dir() else project_root))
from nookara import Client, Instance
from nookara.instance import INSTANCE_OPERATIONS

SESSION = 'instance-session-token'


class Handler(BaseHTTPRequestHandler):
    seen = []

    def log_message(self, *args):
        pass

    def handle_request(self):
        body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        type(self).seen.append((self.command, self.path, dict(self.headers), body))
        path = self.path.split('?')[0]
        out = {'ok': True}
        if path == '/chat/personal-emojis':
            out = {'emojis': [], 'max': 25, 'pro_max': 100} if self.command == 'GET' else {'emoji': {'eid': 'e1', 'name': 'party', 'animated': False}}
        elif path.endswith('/info'):
            out = {'emoji': {'eid': 'e1', 'name': 'party', 'animated': False}, 'server': None, 'personal': {'owner': {'username': 'nat', 'pfp': None}}}
        elif path == '/api/v1/stickers':
            out = {'servers': [{'sid': 's1', 'name': 'Home', 'icon': None, 'stickers': []}]}
        elif path == '/api/v1/servers/s1/stickers':
            out = {'stickers': [], 'max': 30} if self.command == 'GET' else {'sticker': {'tid': 't0123456789', 'name': 'wave', 'animated': False, 'url': 'x'}}
        elif path == '/api/v1/channels/c1/messages':
            out = {'message': {'id': '1', 'sticker': {'tid': 't0123456789'}}}
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(out).encode())

    do_GET = do_POST = do_PATCH = do_DELETE = handle_request


class PersonalEmojiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.url = f'http://127.0.0.1:{cls.server.server_port}'
        cls.client = Client('dummy', base_url=cls.url, allow_insecure=True)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_list(self):
        out = self.client.personal_emojis()
        self.assertEqual(Handler.seen[-1][:2], ('GET', '/chat/personal-emojis'))
        self.assertEqual((out['max'], out['pro_max']), (25, 100))

    def test_add_sends_multipart_with_name(self):
        emoji = self.client.add_personal_emoji(('party.png', b'\x89PNG fake', 'image/png'), 'party')
        method, path, headers, body = Handler.seen[-1]
        self.assertEqual((method, path), ('POST', '/chat/personal-emojis'))
        self.assertIn('multipart/form-data', headers['Content-Type'])
        self.assertIn(b'name="file"', body)
        self.assertIn(b'name="name"', body)
        self.assertIn(b'party', body)
        self.assertEqual(emoji['eid'], 'e1')

    def test_rename_and_delete(self):
        self.client.rename_personal_emoji('e1', 'new_name')
        method, path, _, body = Handler.seen[-1]
        self.assertEqual((method, path, json.loads(body)), ('PATCH', '/chat/personal-emojis/e1', {'name': 'new_name'}))
        self.client.delete_personal_emoji('e1')
        self.assertEqual(Handler.seen[-1][:2], ('DELETE', '/chat/personal-emojis/e1'))

    def test_emoji_info_personal(self):
        out = self.client.emoji_info('e1')
        self.assertEqual(Handler.seen[-1][:2], ('GET', '/chat/emojis/e1/info'))
        self.assertIsNone(out['server'])
        self.assertEqual(out['personal']['owner']['username'], 'nat')


class StickerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.url = f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def instance(self):
        return Instance(self.url, session=SESSION, allow_insecure=True)

    def test_catalogue_has_the_routes(self):
        for op in ('get_api_v1_stickers', 'get_api_v1_servers_by_sid_stickers', 'post_api_v1_servers_by_sid_stickers',
                   'patch_api_v1_servers_by_sid_stickers_by_tid', 'delete_api_v1_servers_by_sid_stickers_by_tid'):
            self.assertIn(op, INSTANCE_OPERATIONS)

    def test_list_and_all(self):
        inst = self.instance()
        self.assertEqual(inst.stickers('s1')['max'], 30)
        self.assertEqual(Handler.seen[-1][:2], ('GET', '/api/v1/servers/s1/stickers'))
        self.assertEqual(inst.all_stickers()[0]['sid'], 's1')
        self.assertEqual(Handler.seen[-1][:2], ('GET', '/api/v1/stickers'))

    def test_add_rename_delete(self):
        inst = self.instance()
        sticker = inst.add_sticker(('wave.png', b'\x89PNG fake', 'image/png'), 'wave', sid='s1')
        method, path, headers, body = Handler.seen[-1]
        self.assertEqual((method, path), ('POST', '/api/v1/servers/s1/stickers'))
        self.assertIn('multipart/form-data', headers['Content-Type'])
        self.assertIn(b'name="name"', body)
        self.assertEqual(sticker['tid'], 't0123456789')
        inst.rename_sticker('t0123456789', 'hi', sid='s1')
        method, path, _, body = Handler.seen[-1]
        self.assertEqual((method, path, json.loads(body)), ('PATCH', '/api/v1/servers/s1/stickers/t0123456789', {'name': 'hi'}))
        inst.delete_sticker('t0123456789', sid='s1')
        self.assertEqual(Handler.seen[-1][:2], ('DELETE', '/api/v1/servers/s1/stickers/t0123456789'))

    def test_send_sticker_has_empty_body(self):
        inst = self.instance()
        out = inst.send_sticker('c1', 't0123456789')
        method, path, _, body = Handler.seen[-1]
        self.assertEqual((method, path), ('POST', '/api/v1/channels/c1/messages'))
        sent = json.loads(body)
        self.assertEqual((sent['message'], sent['sticker']), ('', 't0123456789'))
        self.assertEqual(out['message']['sticker']['tid'], 't0123456789')

    def test_plain_message_has_no_sticker_field(self):
        self.instance().send_message('c1', 'hello')
        self.assertNotIn('sticker', json.loads(Handler.seen[-1][3]))


if __name__ == '__main__':
    unittest.main()
