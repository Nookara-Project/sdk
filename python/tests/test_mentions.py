"""Mention tokens, plain text and message links (nookara.mentions) + link_info."""
import json
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

project_root = Path(__file__).parents[1]
sys.path.insert(0, str(project_root / 'python' if (project_root / 'python').is_dir() else project_root))
from nookara import (Client, Instance, channel_mention, mention, mentions_user, message_link, parse_mentions,
                     parse_message_link, plain_text, role_mention)

SID, CID = 's0123456789', 'c0123456789'


class TokenTests(unittest.TestCase):
    def test_build(self):
        self.assertEqual(mention(42), '<@42>')
        self.assertEqual(mention({'id': 'v:42', 'username': 'nat'}), '<@v:42>')
        self.assertEqual(channel_mention(CID), f'<#{CID}>')
        self.assertEqual(channel_mention({'cid': f'https://chat.example.com|{CID}'}), f'<#{CID}>')
        self.assertEqual(role_mention('rabcdef0123'), '<@&rabcdef0123>')
        for bad in ('nat', '', None, 'x:1'):
            with self.assertRaises(ValueError):
                mention(bad)
        with self.assertRaises(ValueError):
            channel_mention('general')

    def test_parse(self):
        p = parse_mentions(f'hi <@42> and <@v:7> <@42> in <#{CID}> <@&rabcdef0123> <a:wave:e0123456789> @everyone')
        self.assertEqual(p['users'], ['42', 'v:7'])
        self.assertEqual(p['channels'], [CID])
        self.assertEqual(p['roles'], ['rabcdef0123'])
        self.assertEqual(p['emojis'], [{'name': 'wave', 'eid': 'e0123456789', 'animated': True}])
        self.assertTrue(p['everyone'])
        self.assertFalse(p['here'])

    def test_plain_name_is_not_a_mention(self):
        self.assertEqual(parse_mentions('@yell at me for your projects')['users'], [])
        self.assertFalse(mentions_user('@nat hi', 42))
        self.assertTrue(mentions_user('<@42> hi', {'id': 42}))

    def test_plain_text(self):
        t = plain_text(f'<@42> <@9> <#{CID}> <@&rabcdef0123> <:sob:e0123456789>',
                       users={'42': {'username': 'nat', 'display_name': 'Nat'}}, channels=lambda c: 'general', roles={'rabcdef0123': 'Crew'})
        self.assertEqual(t, '@Nat @unknown-user #general @Crew :sob:')

    def test_links(self):
        link = message_link(SID, CID, 123)
        self.assertEqual(link, f'https://ember.nookara.cc/#/s/{SID}/{CID}/123')
        self.assertEqual(parse_message_link(link), {'instance': None, 'sid': SID, 'cid': CID, 'message_id': '123'})
        inst = message_link(SID, CID, instance='https://chat.example.com')
        self.assertEqual(inst, f'https://ember.nookara.cc/#/i/https%3A%2F%2Fchat.example.com/s/{SID}/{CID}')
        self.assertEqual(parse_message_link(inst), {'instance': 'https://chat.example.com', 'sid': SID, 'cid': CID, 'message_id': None})
        self.assertEqual(parse_message_link(f'https://nookara.cc/chat#/s/{SID}/{CID}')['sid'], SID)
        for bad in (f'https://example.com/#/s/{SID}/{CID}', 'https://ember.nookara.cc/#/dm/nat', f'https://ember.nookara.cc/#/s/{SID}/{CID}/abc', 'nope'):
            self.assertIsNone(parse_message_link(bad), bad)


class Handler(BaseHTTPRequestHandler):
    seen = []

    def log_message(self, *args):
        pass

    def do_GET(self):
        type(self).seen.append(self.path)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'server': {'sid': SID, 'name': 'Camp', 'icon': None}, 'channel': {'cid': CID, 'name': 'general'}, 'joined': True}).encode())


class LinkInfoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.base = f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_nookara(self):
        c = Client('dummy', base_url=self.base, allow_insecure=True)
        self.assertEqual(c.link_info(SID, CID)['channel']['name'], 'general')
        self.assertIn(f'/chat/link-info/{SID}/{CID}', Handler.seen)

    def test_instance(self):
        i = Instance(self.base, 'session', allow_insecure=True)
        self.assertEqual(i.link_info(CID, sid=SID)['server']['name'], 'Camp')
        self.assertIn(f'/api/v1/link-info/{SID}/{CID}', Handler.seen)


if __name__ == '__main__':
    unittest.main()
