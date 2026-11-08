"""Channel viewers helper."""
import json
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

project_root = Path(__file__).parents[1]
sys.path.insert(0, str(project_root / 'python' if (project_root / 'python').is_dir() else project_root))
from nookara import Client


class Handler(BaseHTTPRequestHandler):
    seen = []

    def log_message(self, *args):
        pass

    def do_GET(self):
        type(self).seen.append((self.command, self.path))
        out = {'all': True} if self.path.endswith('/open/viewers') else {'all': False, 'ids': ['12', '40']}
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(out).encode())


class ChannelViewersTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.client = Client('dummy', base_url=f'http://127.0.0.1:{cls.server.server_port}', allow_insecure=True)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_limited(self):
        out = self.client.channel_viewers('abc123')
        self.assertEqual(Handler.seen[-1], ('GET', '/chat/channels/abc123/viewers'))
        self.assertEqual(out, {'all': False, 'ids': ['12', '40']})

    def test_everyone(self):
        self.assertEqual(self.client.channel_viewers('open'), {'all': True})
        self.assertEqual(Handler.seen[-1], ('GET', '/chat/channels/open/viewers'))


if __name__ == '__main__':
    unittest.main()
