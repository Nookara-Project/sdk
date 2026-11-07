"""Inbox helpers: mentions, saved messages, translate and cancelling a friend request."""
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
    outgoing = [{'id': 7, 'to_username': 'Alice'}]

    def log_message(self, *args):
        pass

    def handle_request(self):
        body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        type(self).seen.append((self.command, self.path, json.loads(body) if body else None))
        out = {'ok': True}
        if self.path == '/chat/saved' and self.command == 'POST':
            out = {'ok': True, 'id': '88'}
        elif self.path == '/chat/saved/check':
            out = {'saved': {'123': '88'}}
        elif self.path == '/chat/translate':
            out = {'text': 'Hello!', 'from': 'fr', 'to': 'en'}
        elif self.path == '/friends/requests':
            out = {'incoming': [], 'outgoing': type(self).outgoing}
        elif self.path.startswith('/friends/request/'):
            out = {'success': True}
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(out).encode())

    do_GET = do_POST = do_DELETE = handle_request


class InboxTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.client = Client('dummy', base_url=f'http://127.0.0.1:{cls.server.server_port}', allow_insecure=True)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_mentions_and_saved_lists(self):
        self.client.inbox_mentions(before=50, limit=20)
        self.assertEqual(Handler.seen[-1][:2], ('GET', '/chat/inbox/mentions?before=50&limit=20'))
        self.client.inbox_mentions()
        self.assertEqual(Handler.seen[-1][1], '/chat/inbox/mentions')
        self.client.saved_messages(limit=5)
        self.assertEqual(Handler.seen[-1][:2], ('GET', '/chat/saved?limit=5'))

    def test_save_unsave_check(self):
        self.assertEqual(self.client.save_message('channel', 123), '88')
        self.assertEqual(Handler.seen[-1], ('POST', '/chat/saved', {'kind': 'channel', 'id': '123'}))
        snap = {'room': 'grp_x', 'room_name': 'g', 'user': 'bob', 'message': 'hi', 'created_at': 1, 'id': 'a'}
        self.client.save_message('group', snapshot=snap)
        self.assertEqual(Handler.seen[-1][2], {'kind': 'group', 'snapshot': snap})
        with self.assertRaises(ValueError): self.client.save_message('group')
        with self.assertRaises(ValueError): self.client.save_message('nope', 1)
        with self.assertRaises(ValueError): self.client.save_message('dm')
        self.assertEqual(self.client.saved_ids('channel', [123, 124]), {'123': '88'})
        self.assertEqual(Handler.seen[-1][2], {'kind': 'channel', 'ids': ['123', '124']})
        self.client.unsave_message('88')
        self.assertEqual(Handler.seen[-1][:2], ('DELETE', '/chat/saved/88'))

    def test_translate(self):
        self.assertEqual(self.client.translate('Bonjour!', 'en')['text'], 'Hello!')
        self.assertEqual(Handler.seen[-1], ('POST', '/chat/translate', {'text': 'Bonjour!', 'to': 'en'}))
        self.client.translate('x', 'pt-BR', source='en')
        self.assertEqual(Handler.seen[-1][2], {'text': 'x', 'to': 'pt-BR', 'from': 'en'})

    def test_cancel_friend_request(self):
        self.assertTrue(self.client.cancel_friend_request('alice'))
        self.assertEqual(Handler.seen[-1][:2], ('DELETE', '/friends/request/7'))
        count = len(Handler.seen)
        self.assertFalse(self.client.cancel_friend_request('nobody'))
        self.assertEqual(len(Handler.seen), count + 1)


if __name__ == '__main__':
    unittest.main()
