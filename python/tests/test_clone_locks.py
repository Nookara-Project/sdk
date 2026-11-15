"""Clone locks: lock_my_emojis, clone_check, and `from` on personal emoji / sticker uploads."""
import hashlib
import json
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

project_root = Path(__file__).parents[1]
sys.path.insert(0, str(project_root / 'python' if (project_root / 'python').is_dir() else project_root))
from nookara import Client

LOCKED = b'\x89PNG locked one'


class Handler(BaseHTTPRequestHandler):
    seen = []

    def log_message(self, *args):
        pass

    def handle_request(self):
        body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        type(self).seen.append((self.command, self.path, dict(self.headers), body))
        u = urlsplit(self.path)
        out, code = {'ok': True}, 200
        if u.path == '/chat/clone-check':
            sha = parse_qs(u.query).get('sha256', [''])[0]
            out = {'locked': True, 'reason': 'clone_locked'} if sha == hashlib.sha256(LOCKED).hexdigest() else {'locked': False}
        elif u.path == '/chat/settings':
            out = {'settings': {'lock_emojis': json.loads(body)['lock_emojis']}}
        elif u.path == '/chat/personal-emojis':
            out, code = ({'error': 'clone_locked'}, 403) if LOCKED in body else ({'emoji': {'eid': 'e0123456789'}}, 200)
        elif u.path == '/chat/personal-stickers':
            out = {'sticker': {'sid': 's0123456789'}}
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(out).encode())

    do_GET = do_POST = do_PATCH = handle_request


class CloneLockTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.client = Client('dummy', base_url=f'http://127.0.0.1:{cls.server.server_port}', allow_insecure=True)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_lock_my_emojis(self):
        out = self.client.lock_my_emojis()
        method, path, _, body = Handler.seen[-1]
        self.assertEqual((method, path, json.loads(body)), ('PATCH', '/chat/settings', {'lock_emojis': True}))
        self.assertTrue(out['settings']['lock_emojis'])
        self.client.lock_my_emojis(False)
        self.assertEqual(json.loads(Handler.seen[-1][3]), {'lock_emojis': False})

    def test_clone_check_takes_bytes_or_a_hash(self):
        self.assertEqual(self.client.clone_check(LOCKED), {'locked': True, 'reason': 'clone_locked'})
        self.assertIn('sha256=' + hashlib.sha256(LOCKED).hexdigest(), Handler.seen[-1][1])
        self.assertEqual(self.client.clone_check(hashlib.sha256(b'other').hexdigest(), velora_id=42), {'locked': False})
        self.assertIn('velora_id=42', Handler.seen[-1][1])

    def test_uploads_send_from(self):
        self.client.add_personal_sticker(('wave.png', b'\x89PNG x', 'image/png'), 'wave', source='https://camp.example/uploads/stickers/t1.png')
        body = Handler.seen[-1][3]
        self.assertIn(b'name="from"', body)
        self.assertIn(b'https://camp.example/uploads/stickers/t1.png', body)
        self.client.add_personal_emoji(('wave.png', b'\x89PNG x', 'image/png'))
        self.assertNotIn(b'name="from"', Handler.seen[-1][3])

    def test_locked_upload_raises(self):
        with self.assertRaises(Exception) as cm:
            self.client.add_personal_emoji(('wave.png', LOCKED, 'image/png'), 'wave')
        self.assertIn('clone_locked', str(cm.exception))


if __name__ == '__main__':
    unittest.main()
