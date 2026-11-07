"""Ember Beta status helpers."""
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

    def handle_request(self):
        type(self).seen.append((self.command, self.path))
        out = {'beta': True, 'membership': {'status': 'active', 'period': 'monthly', 'current_period_end': 1, 'cancel_at_period_end': False, 'test': False}, 'product': None}
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(out).encode())

    do_GET = do_POST = handle_request


class EmberBetaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.client = Client('dummy', base_url=f'http://127.0.0.1:{cls.server.server_port}', allow_insecure=True)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_status(self):
        out = self.client.ember_beta()
        self.assertEqual(Handler.seen[-1], ('GET', '/chat/beta'))
        self.assertTrue(out['beta'])
        self.assertEqual(out['membership']['status'], 'active')

    def test_refresh(self):
        self.assertTrue(self.client.refresh_ember_beta()['beta'])
        self.assertEqual(Handler.seen[-1], ('POST', '/chat/beta/refresh'))


if __name__ == '__main__':
    unittest.main()
