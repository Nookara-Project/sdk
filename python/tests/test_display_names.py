"""Display name helpers (0.9.7)."""
import json
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

project_root = Path(__file__).parents[1]
sys.path.insert(0, str(project_root / 'python' if (project_root / 'python').is_dir() else project_root))
import nookara
from nookara import Client


class Handler(BaseHTTPRequestHandler):
    seen = []

    def log_message(self, *args):
        pass

    def _send(self, code, out):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(out).encode())

    def do_PATCH(self):
        body = json.loads(self.rfile.read(int(self.headers.get('Content-Length') or 0)) or b'{}')
        type(self).seen.append((self.command, self.path, body))
        if body.get('display_name') == 'Nookara':
            return self._send(400, {'error': 'display_name_reserved'})
        self._send(200, {'success': True, 'display_name': body.get('display_name')})

    def do_GET(self):
        type(self).seen.append((self.command, self.path, None))
        self._send(200, {'account': {'id': 1, 'username': 'nat', 'display_name': 'Nat'}})


class DisplayNameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.client = Client('dummy', base_url=f'http://127.0.0.1:{cls.server.server_port}', allow_insecure=True)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_set_and_clear(self):
        self.assertEqual(self.client.set_display_name('Nat'), {'success': True, 'display_name': 'Nat'})
        self.assertEqual(Handler.seen[-1], ('PATCH', '/account/update', {'display_name': 'Nat'}))
        self.client.clear_display_name()
        self.assertEqual(Handler.seen[-1], ('PATCH', '/account/update', {'display_name': None}))
        self.client.set_display_name('')
        self.assertEqual(Handler.seen[-1][2], {'display_name': None})

    def test_refused(self):
        with self.assertRaises(nookara.APIError) as cm:
            self.client.set_display_name('Nookara')
        self.assertIn('display_name_reserved', str(cm.exception.args) + str(getattr(cm.exception, 'code', '')) + str(getattr(cm.exception, 'error', '')))

    def test_own(self):
        self.assertEqual(self.client.display_name(), 'Nat')

    def test_shown_name(self):
        self.assertEqual(nookara.shown_name({'username': 'nat', 'display_name': 'Nat'}), 'Nat')
        self.assertEqual(nookara.shown_name({'username': 'nat', 'display_name': None}), 'nat')
        self.assertEqual(nookara.shown_name({'username': 'nat', 'display_name': '  '}), 'nat')
        self.assertEqual(nookara.shown_name(None), '')


if __name__ == '__main__':
    unittest.main()