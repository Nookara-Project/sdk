"""Personal stickers (Nookara /chat/personal-stickers) and the sticker message text."""
import json
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

project_root = Path(__file__).parents[1]
sys.path.insert(0, str(project_root / 'python' if (project_root / 'python').is_dir() else project_root))
from nookara import Client

STICKER = {'sid': 's0123456789', 'name': 'wave', 'animated': False, 'url': 'https://nookara.cc/uploads/stickers/s0123456789.png',
           'send': 'https://nookara.cc/uploads/stickers/s0123456789.png#wave'}


class Handler(BaseHTTPRequestHandler):
    seen = []

    def log_message(self, *args):
        pass

    def handle_request(self):
        body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        type(self).seen.append((self.command, self.path, dict(self.headers), body))
        path = self.path.split('?')[0]
        out = {'ok': True}
        if path == '/chat/personal-stickers':
            out = {'stickers': [STICKER], 'max': 10, 'pro_max': 50} if self.command == 'GET' else {'sticker': STICKER}
        elif path.endswith('/info'):
            out = {'sticker': STICKER, 'owner': {'username': 'nat', 'pfp': None}}
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(out).encode())

    do_GET = do_POST = do_PATCH = do_DELETE = handle_request


class PersonalStickerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.client = Client('dummy', base_url=f'http://127.0.0.1:{cls.server.server_port}', allow_insecure=True)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_list(self):
        out = self.client.personal_stickers()
        self.assertEqual(Handler.seen[-1][:2], ('GET', '/chat/personal-stickers'))
        self.assertEqual((out['max'], out['pro_max']), (10, 50))

    def test_add_sends_multipart_with_name(self):
        s = self.client.add_personal_sticker(('wave.png', b'\x89PNG fake', 'image/png'), 'wave')
        method, path, headers, body = Handler.seen[-1]
        self.assertEqual((method, path), ('POST', '/chat/personal-stickers'))
        self.assertIn('multipart/form-data', headers['Content-Type'])
        self.assertIn(b'name="file"', body)
        self.assertIn(b'name="name"', body)
        self.assertEqual(s['sid'], 's0123456789')

    def test_rename_delete_info(self):
        self.client.rename_personal_sticker('s0123456789', 'hi')
        method, path, _, body = Handler.seen[-1]
        self.assertEqual((method, path, json.loads(body)), ('PATCH', '/chat/personal-stickers/s0123456789', {'name': 'hi'}))
        self.client.delete_personal_sticker('s0123456789')
        self.assertEqual(Handler.seen[-1][:2], ('DELETE', '/chat/personal-stickers/s0123456789'))
        out = self.client.personal_sticker_info('s0123456789')
        self.assertEqual(Handler.seen[-1][:2], ('GET', '/chat/personal-stickers/s0123456789/info'))
        self.assertEqual(out['owner']['username'], 'nat')


class StickerTextTests(unittest.TestCase):
    def test_text_round_trip(self):
        text = Client.personal_sticker_text(STICKER)
        self.assertEqual(text, STICKER['send'])
        self.assertEqual(Client.personal_sticker_text({k: v for k, v in STICKER.items() if k != 'send'}), STICKER['send'])
        self.assertEqual(Client.parse_personal_sticker(text), {'sid': 's0123456789', 'name': 'wave', 'url': STICKER['url'], 'animated': False})
        self.assertTrue(Client.parse_personal_sticker('https://cdn.nookara.cc/uploads/stickers/sabcdefabcd.gif')['animated'])

    def test_not_a_sticker(self):
        for t in ['hi ' + STICKER['send'], 'https://evil.example/uploads/stickers/s0123456789.png', 'https://nookara.cc/uploads/emojis/e0123456789.png', '', None]:
            self.assertIsNone(Client.parse_personal_sticker(t))


if __name__ == '__main__':
    unittest.main()
