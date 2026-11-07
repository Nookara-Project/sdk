"""Bonfire additions of 0.4.0: scopes that are only requested, ScopeError, instance scopes, invites,
uploads, signature verification, the account hub and the multi-instance bot program."""
import asyncio
import base64
import json
import sys
import threading
import unittest
import warnings
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

project_root = Path(__file__).parents[1]
sys.path.insert(0, str(project_root / 'python' if (project_root / 'python').is_dir() else project_root))
from nookara import (APIError, Ember, BotProgram, Client, Instance, ScopeError, Signer, TransportError, login,
                        scope_mask, scope_names, has_scope, verify_message, EMBER_APP_MASK, SCOPES)
from nookara import signing
from nookara.client import login as client_login


def b64(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode()


def ticket(scp):
    """An unsigned stand-in for an instance ticket; the library only reads the scp claim."""
    return b64(b'{"alg":"EdDSA"}') + '.' + b64(json.dumps({'scp': scp}).encode()) + '.sig'


class Handler(BaseHTTPRequestHandler):
    seen = []
    responses = {}

    def log_message(self, *args):
        pass

    def do_GET(self):
        content = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        type(self).seen.append((self.command, self.path, dict(self.headers), content))
        status, body = type(self).responses.get((self.command, self.path.split('?')[0]), (200, {'ok': True}))
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())
    do_POST = do_PUT = do_PATCH = do_DELETE = do_GET


class ScopeTests(unittest.TestCase):
    def test_scope_masks(self):
        self.assertEqual(scope_mask('PROFILE_READ', 'CHAT'), 2049)
        self.assertEqual(scope_mask('Chat Messaging', 'Upload Media', 4), 2048 | 4096 | 4)
        self.assertEqual(scope_names(2049), ['PROFILE_READ', 'CHAT'])
        self.assertTrue(has_scope(2049, 'CHAT'))
        self.assertFalse(has_scope(2049, 'MEDIA_UPLOAD'))
        with self.assertRaises(ValueError):
            scope_mask('NOT_A_SCOPE')
        with self.assertRaises(ValueError):
            scope_mask(3)
        self.assertEqual(sorted(SCOPES.values()), sorted(1 << i for i in range(22)))  # (16 legacy bits + Manage Files, notifications, blocked people)
        self.assertEqual(EMBER_APP_MASK & 2048, 2048)

    def test_login_requests_scopes_and_reserves_bonfire_names(self):
        with patch('nookara.client.Client') as client, patch('nookara.client.time.sleep'):
            client.return_value.post_auth_ext_code.return_value = {'code': 'c'}
            client.return_value.get_auth_ext_code_status.return_value = {'ready': True, 'token': 'tok'}
            urls = []
            self.assertEqual(client_login(scopes=scope_mask('PROFILE_READ', 'CHAT'), on_url=urls.append), 'tok')
            self.assertEqual(client.return_value.post_auth_ext_code.call_args.kwargs['json']['permissions_integer'], 2049 << 16)
            self.assertIn('permissions=' + str(2049 << 16), urls[0])
        for bad in [dict(scopes=0), dict(scopes=70000), dict(project_name='Bonfire (desktop app)'), dict(scopes=-1)]:
            with self.assertRaises(ValueError):
                client_login(on_url=lambda url: None, **bad)

    def test_client_reports_granted_scopes(self):
        c = Client('t', base_url='http://127.0.0.1:1', allow_insecure=True)
        with patch.object(c, 'get_bonfire_session', return_value={'granted': 2049 | 4096, 'effective': 2049, 'disabled': 4096}):
            self.assertEqual(c.granted_scopes(), 2049)
            self.assertEqual(c.scope_names(), ['PROFILE_READ', 'CHAT'])
            self.assertTrue(c.has_scope('CHAT'))
            self.assertFalse(c.has_scope('Upload Media'))
            self.assertEqual(c.require_scope('CHAT'), 2048)
            with self.assertRaises(ScopeError) as caught:
                c.require_scope('MEDIA_UPLOAD')
            self.assertEqual(caught.exception.scope, 'MEDIA_UPLOAD')
            self.assertEqual(caught.exception.label, 'Upload Media')
            self.assertIsInstance(caught.exception, APIError)


class Server:
    @classmethod
    def start(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def stop(cls):
        cls.server.shutdown()
        cls.server.server_close()


class ScopeErrorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Server.start.__func__(cls)

    @classmethod
    def tearDownClass(cls):
        Server.stop.__func__(cls)

    def setUp(self):
        Handler.seen.clear()
        Handler.responses = {}

    def test_insufficient_scope_becomes_scope_error(self):
        Handler.responses[('GET', '/account/me')] = (403, {'error': 'insufficient_scope', 'required_scope': 4096, 'disabled_by_admin': False})
        Handler.responses[('GET', '/chat/settings')] = (403, {'error': 'scope_disabled', 'required_scope': 2048, 'disabled_by_admin': True})
        Handler.responses[('GET', '/chat/presence/x')] = (403, {'error': 'account_suspended'})
        c = Client('t', base_url=self.base, allow_insecure=True)
        with self.assertRaises(ScopeError) as caught:
            c.get_account_me()
        err = caught.exception
        self.assertEqual((err.status, err.error, err.scope, err.required_scope, err.disabled_by_admin), (403, 'insufficient_scope', 'MEDIA_UPLOAD', 4096, False))
        with self.assertRaises(ScopeError) as caught:
            c.get_chat_settings()
        self.assertTrue(caught.exception.disabled_by_admin)
        with self.assertRaises(APIError) as caught:
            c.get_chat_presence_by_username(username='x')
        self.assertNotIsInstance(caught.exception, ScopeError)

    def test_error_extras(self):
        exc = APIError(403, {'error': 'server_read_only', 'moved_to': 'https://chat.ikelene.net', 'reason': 'x'})
        self.assertEqual((exc.moved_to, exc.reason, exc.required_scope), ('https://chat.ikelene.net', 'x', None))

    def test_legacy_helpers_warn(self):
        Handler.responses[('GET', '/chat/servers')] = (200, {'servers': []})
        c = Client('t', base_url=self.base, allow_insecure=True)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            c.servers()
        self.assertTrue(any(issubclass(w.category, DeprecationWarning) for w in caught))


class InstanceScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Server.start.__func__(cls)

    @classmethod
    def tearDownClass(cls):
        Server.stop.__func__(cls)

    def setUp(self):
        Handler.seen.clear()
        Handler.responses = {
            ('POST', '/api/v1/auth/velora'): (200, {'session': 'SESS', 'user': {'id': 'v:7', 'kind': 'velora', 'velora_id': '7', 'username': 'nat'}}),
            ('GET', '/.well-known/bonfire'): (200, {'software': 'bonfire-server', 'protocol': 1, 'accounts_mode': 'velora', 'features': {'signing': True, 'uploads': True},
                                                    'build': {'version': '0.1.0', 'commit': None}, 'read_only': False, 'community': {'sid': 'sC', 'name': 'Home'}}),
        }

    def nookara(self, scp):
        nookara = Client('velora-secret', base_url='http://127.0.0.1:1', allow_insecure=True)
        patcher = patch.object(nookara, 'post_bonfire_instance_token', return_value={'token': ticket(scp)})
        patcher.start()
        self.addCleanup(patcher.stop)
        return nookara

    def instance(self):
        return Instance(self.base, allow_insecure=True)

    def test_discovery_properties(self):
        inst = self.instance()
        self.assertEqual(inst.accounts_mode, 'velora')
        self.assertTrue(inst.features['signing'])
        self.assertEqual(inst.build['version'], '0.1.0')
        self.assertFalse(inst.read_only)
        self.assertEqual(inst.community_id(), 'sC')
        Handler.responses[('GET', '/.well-known/bonfire')] = (200, {'name': 'something else'})
        with self.assertRaises(ValueError):
            self.instance().discover()

    def test_ticket_scopes_are_kept_and_media_is_checked_early(self):
        inst = self.instance()
        inst.login_with_nookara(self.nookara(['chat']))
        self.assertEqual(inst.scopes, ['chat'])
        self.assertTrue(inst.has_scope('CHAT'))
        self.assertFalse(inst.has_scope('media'))
        Handler.seen.clear()
        with self.assertRaises(ScopeError):
            inst.upload(('a.txt', b'hello', 'text/plain'))
        with self.assertRaises(ScopeError):
            inst.import_media('https://example.com/a.png')
        self.assertEqual(Handler.seen, [])

    def test_media_calls_when_allowed(self):
        inst = self.instance()
        inst.login_with_nookara(self.nookara(['chat', 'media']))
        Handler.seen.clear()
        inst.upload(('a.txt', b'hello', 'text/plain'), cid='c1')
        self.assertEqual(Handler.seen[-1][1], '/api/v1/media/upload?sid=sC&cid=c1')
        inst.import_media('https://example.com/a.png', name='a.png', cid='c1')
        method, path, _, body = Handler.seen[-1]
        self.assertEqual((method, path), ('POST', '/api/v1/media/import?sid=sC&cid=c1'))
        self.assertEqual(json.loads(body), {'url': 'https://example.com/a.png', 'name': 'a.png'})

    def test_sign_auto_skips_when_declined_and_true_raises(self):
        inst = self.instance()
        nookara = self.nookara(['chat'])
        with patch.object(nookara, 'get_bonfire_signing_key', side_effect=ScopeError(403, {'error': 'insufficient_scope', 'required_scope': 32768})) as key:
            inst.login_with_nookara(nookara, sign='auto')
            key.assert_not_called()
            self.assertIsNone(inst.signer)
            with self.assertRaises(ScopeError):
                self.instance().login_with_nookara(nookara, sign=True)

    def test_scopes_fetched_from_me_when_not_from_a_ticket(self):
        Handler.responses[('GET', '/api/v1/me')] = (200, {'user': {}, 'scopes': ['chat', 'voice']})
        inst = Instance(self.base, 'SESSION', allow_insecure=True)
        self.assertEqual(inst.scopes, ['chat', 'voice'])
        self.assertTrue(inst.has_scope('VOICE'))

    def test_invite_and_channel_helpers(self):
        inst = Instance(self.base, 'SESSION', allow_insecure=True)
        inst._community = 'sC'
        Handler.responses[('GET', '/api/v1/servers/sC/invites')] = (200, {'invites': [{'code': 'abc'}]})
        Handler.responses[('GET', '/api/v1/servers/sC/requests')] = (200, {'requests': [{'user': {'id': 'v:9'}}]})
        self.assertEqual(inst.invites(), [{'code': 'abc'}])
        self.assertEqual(inst.join_requests()[0]['user']['id'], 'v:9')
        inst.create_invite(expires_in=3600, max_uses=5)
        self.assertEqual(json.loads(Handler.seen[-1][3]), {'expires_in': 3600, 'max_uses': 5})
        inst.delete_invite('abc')
        self.assertEqual(Handler.seen[-1][:2], ('DELETE', '/api/v1/invites/abc'))
        inst.invite_info('abc')
        self.assertEqual(Handler.seen[-1][1], '/api/v1/invite/abc')
        inst.accept_join_request('v:9')
        self.assertEqual(Handler.seen[-1][:2], ('POST', '/api/v1/servers/sC/requests/v%3A9/accept'))
        inst.create_channel('news', type='logs', config={})
        self.assertEqual(json.loads(Handler.seen[-1][3]), {'name': 'news', 'type': 'logs', 'config': {}})
        inst.kick('v:9', ban=True)
        self.assertEqual(Handler.seen[-1][1], '/api/v1/servers/sC/members/v%3A9?ban=1')
        inst.set_notify('sC', level='mentions')
        self.assertEqual(json.loads(Handler.seen[-1][3]), {'level': 'mentions', 'mute_minutes': 0, 'push': True})
        Handler.responses[('GET', '/api/v1/identities')] = (200, {'users': []})
        inst.identities(['v:1', 'b:2'])
        self.assertEqual(Handler.seen[-1][1], '/api/v1/identities?ids=v%3A1%2Cb%3A2')

    def test_game_and_admin_helpers(self):
        inst = Instance(self.base, 'SESSION', allow_insecure=True)
        inst._community = 'sC'
        inst.game_link('g1', cid='c9')
        self.assertEqual(Handler.seen[-1][:2], ('POST', '/api/v1/game/connected/g1/link'))
        inst.game_connected(q='mc')
        self.assertEqual(Handler.seen[-1][1], '/api/v1/game/connected?q=mc')
        inst.claim('ABCD-EFGH')
        self.assertEqual(json.loads(Handler.seen[-1][3]), {'code': 'ABCD-EFGH'})
        inst.import_from_nookara('bit_x')
        self.assertEqual(Handler.seen[-1][:2], ('POST', '/api/v1/import/velora'))
        inst.instance_info()
        self.assertEqual(Handler.seen[-1][1], '/api/v1/instance/info')
        Handler.responses[('GET', '/api/v1/instance/info')] = (200, {'update': {'outdated': True}})
        self.assertTrue(inst.update_available())


class VerifyTests(unittest.TestCase):
    def make_message(self, signer, **extra):
        fields = dict(instance='https://chat.example', community='sC', channel='cC', author='7', body='Hello', attachments=['a' * 64])
        fields.update(extra)
        sig = signer.sign(**fields)
        message = {'id': '55', 'server': 'sC', 'channel': 'cC', 'author': {'id': 'v:7', 'velora_id': '7'}, 'body': 'Hello',
                   'attachments': [{'sha256': 'a' * 64, 'url': 'https://chat.example/uploads/x'}], 'reply_to': extra.get('reply_to'),
                   'edited_at': 1 if extra.get('edit_of') else None, 'signature': sig}
        return message, sig

    def key_pair(self):
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
        from cryptography.hazmat.primitives import serialization
        private = Ed25519PrivateKey.generate()
        der = private.private_bytes(serialization.Encoding.DER, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
        raw = private.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
        return b64(der), b64(raw)

    def test_verify_message(self):
        private, public = self.key_pair()
        signer = Signer('k_test', private, iss='https://velora.example', public_key=public)
        key = {'kid': 'k_test', 'user_id': '7', 'public_key': public, 'revoked_at': None}
        message, sig = self.make_message(signer)
        self.assertEqual(verify_message(message, key, iss='https://velora.example', instance='https://chat.example'), (True, 'ok'))
        tampered = dict(message, body='Hello!')
        self.assertEqual(verify_message(tampered, key, iss='https://velora.example', instance='https://chat.example'), (False, 'bad_signature'))
        self.assertEqual(verify_message(message, dict(key, user_id='8'), iss='https://velora.example', instance='https://chat.example'), (False, 'wrong_user'))
        self.assertEqual(verify_message(message, dict(key, revoked_at=sig['ts'] - 1), iss='https://velora.example', instance='https://chat.example'), (False, 'revoked'))
        self.assertEqual(verify_message(dict(message, signature=None), key, iss='https://velora.example', instance='https://chat.example'), (False, 'unsigned'))
        edited, _ = self.make_message(signer, edit_of='55', reply_to='54')
        self.assertEqual(verify_message(edited, key, iss='https://velora.example', instance='https://chat.example'), (True, 'ok'))

    def test_klipy_attachment_refs(self):
        refs = signing.attachment_refs([{'url': 'https://media.klipy.com/a.gif'}, {'sha256': 'b' * 64}, 'c' * 64])
        self.assertEqual(refs, ['url:https://media.klipy.com/a.gif', 'b' * 64, 'c' * 64])
        with self.assertRaises(ValueError):
            signing.attachment_refs([{'url': 'https://evil.example/a.gif'}])


class FakeNookara:
    base_url = 'https://velora.example'

    def __init__(self, urls, default_joined=True):
        self.urls = urls
        self.saved = None
        self.joined_default = None

    def ember_instances(self):
        return [{'url': u} for u in self.urls]

    def sync_ember_instances(self, local):
        self.urls = list(dict.fromkeys(self.urls + [normalize(u) for u in local]))
        return self.urls

    def set_ember_instances(self, urls):
        self.urls = list(urls)
        return self.urls

    def get_bonfire_instances(self):
        return {'default_instance': 'https://chat.example', 'instances': [{'url': 'https://chat.example', 'auto_join': True}]}

    def ember_default_joined(self, url=None):
        self.joined_default = url


def normalize(u):
    from nookara import normalize_origin
    return normalize_origin(u)


class FakeInstance:
    def __init__(self, url, mode='velora', fail=None, community=None):
        self.url, self.accounts_mode, self.fail, self.community = url, mode, fail, community
        self.info = {'read_only': False}
        self.joined = False

    def login_with_nookara(self, nookara, sign=False):
        if self.fail:
            raise self.fail

    def joined_communities(self):
        return [self.community] if self.community else []

    def join(self):
        self.joined = True
        return {'sid': 's'}

    def logout(self):
        pass


class HubTests(unittest.TestCase):
    def test_communities_report_per_server_problems(self):
        fakes = {
            'https://a.example': FakeInstance('https://a.example', community={'name': 'A'}),
            'https://down.example': FakeInstance('https://down.example', fail=TransportError('x')),
            'https://local.example': FakeInstance('https://local.example', mode='local'),
            'https://nochat.example': FakeInstance('https://nochat.example', fail=ScopeError(403, {'error': 'insufficient_scope'})),
            'https://banned.example': FakeInstance('https://banned.example', fail=APIError(403, {'error': 'instance_banned'})),
        }
        nookara = FakeNookara(list(fakes))
        hub = Ember(nookara, instance_factory=lambda url: fakes[url])
        result = {item['instance']: item for item in hub.communities()}
        self.assertEqual(result['https://a.example']['community'], {'name': 'A'})
        self.assertEqual(result['https://down.example']['error'], 'unreachable')
        self.assertEqual(result['https://local.example']['error'], 'local_accounts')
        self.assertEqual(result['https://nochat.example']['error'], 'chat_scope_missing')
        self.assertEqual(result['https://banned.example']['error'], 'instance_banned')

    def test_add_remove_and_default_join(self):
        fakes = {'https://chat.example': FakeInstance('https://chat.example')}
        nookara = FakeNookara(['https://chat.example'])
        hub = Ember(nookara, instance_factory=lambda url: fakes[url])
        self.assertEqual(hub.add('https://New.Example:443/x'), ['https://chat.example', 'https://new.example'])
        self.assertEqual(hub.remove('https://new.example'), ['https://chat.example'])
        self.assertEqual(hub.join_default(), {'sid': 's'})
        self.assertEqual(nookara.joined_default, 'https://chat.example')
        self.assertTrue(fakes['https://chat.example'].joined)


class FakeGateway:
    def __init__(self, events, fail=None):
        self.events, self.fail, self.closed = events, fail, False

    async def start(self):
        if self.fail:
            raise self.fail

    def __aiter__(self):
        return self._iter()

    async def _iter(self):
        for event in self.events:
            yield event
        await asyncio.sleep(3600)

    async def close(self):
        self.closed = True


class FakeProgram(BotProgram):
    def __init__(self, installs, *args, **kwargs):
        super().__init__('bot-token', *args, **kwargs)
        self.install_list = installs

    def installs(self):
        return list(self.install_list)


class BotProgramTests(unittest.IsolatedAsyncioTestCase):
    async def test_one_gateway_per_install_and_merged_events(self):
        gateways = {
            'https://a.example': FakeGateway([{'type': 'MESSAGE_CREATE', 'data': {'content': 'hi'}, 'seq': 1}]),
            'https://b.example': FakeGateway([{'type': 'MESSAGE_CREATE', 'data': {'content': 'yo'}, 'seq': 1}]),
        }
        program = FakeProgram(list(gateways), instance_factory=lambda origin: Instance(origin, bot_token='bot-token'),
                              gateway_factory=lambda inst: gateways[inst.url], poll_interval=3600)
        seen = {}
        async with program:
            while len(seen) < 2:
                event = await asyncio.wait_for(program.__anext__(), 2)
                if event['type'] == 'MESSAGE_CREATE':
                    seen[event['instance']] = event['data']['content']
            self.assertEqual(program.origins, ['https://a.example', 'https://b.example'])
        self.assertEqual(seen, {'https://a.example': 'hi', 'https://b.example': 'yo'})
        self.assertTrue(all(g.closed for g in gateways.values()))

    async def test_refresh_adds_removes_and_isolates_failures(self):
        gateways = {
            'https://a.example': FakeGateway([]),
            'https://dead.example': FakeGateway([], fail=APIError(403, {'error': 'banned'})),
            'https://c.example': FakeGateway([]),
        }
        program = FakeProgram(['https://a.example', 'https://dead.example'], instance_factory=lambda origin: Instance(origin, bot_token='bot-token'),
                              gateway_factory=lambda inst: gateways[inst.url], poll_interval=3600)
        async with program:
            await asyncio.sleep(0.05)
            self.assertEqual(program.errors.get('https://dead.example'), 'banned')
            program.install_list = ['https://a.example', 'https://c.example']
            await program.refresh()
            self.assertEqual(program.origins, ['https://a.example', 'https://c.example'])
            self.assertTrue(gateways['https://dead.example'].closed)

    def test_installs_filters_test_installs(self):
        program = BotProgram('bot-token')
        with patch.object(program._nookara, 'bot_installs', return_value=[{'origin': 'https://a.example/', 'test': False}, {'origin': 'https://t.example', 'test': True}, {'origin': 'nonsense'}]):
            self.assertEqual(program.installs(), ['https://a.example'])
            program.include_test = True
            self.assertEqual(program.installs(), ['https://a.example', 'https://t.example'])

    def test_nookara_bot_installs_request(self):
        program = BotProgram('bot-token')
        with patch.object(program._nookara, 'request', return_value={'instances': []}) as req:
            program._nookara.bot_installs()
            self.assertEqual(req.call_args[0], ('GET', '/bonfire/bots/self/installs'))
            self.assertTrue(req.call_args[1]['auth'])


class PublicDispatchTests(unittest.TestCase):
    def test_velora_helpers_dispatch(self):
        c = Client('t', base_url='http://127.0.0.1:1', allow_insecure=True)
        with patch.object(c, 'request', return_value={'profiles': [], 'keys': [], 'scopes': [], 'instances': [], 'platforms': [], 'guilds': []}) as req:
            c.ember_profiles([1, 2]); self.assertEqual((req.call_args[0], req.call_args[1]['query']), (('GET', '/bonfire/profiles'), {'ids': '1,2'}))
            c.ember_key('k_1'); self.assertEqual(req.call_args[0], ('GET', '/bonfire/keys/kid/k_1'))
            c.ember_user_keys(5); self.assertEqual(req.call_args[0], ('GET', '/bonfire/keys/user/5'))
            c.ember_jwks(); self.assertEqual(req.call_args[0], ('GET', '/.well-known/bonfire/jwks.json'))
            c.server_latest(); self.assertEqual(req.call_args[0], ('GET', '/bonfire/server-latest.json'))
            c.ember_scopes(); self.assertEqual(req.call_args[0], ('GET', '/bonfire/scopes.json'))
            c.ember_default_joined('https://chat.ikelene.net'); self.assertEqual((req.call_args[0], req.call_args[1]['json']), (('POST', '/bonfire/instances/default-joined'), {'url': 'https://chat.ikelene.net'}))
            c.ember_instance_prefs('https://chat.ikelene.net', muted=True); self.assertEqual((req.call_args[0], req.call_args[1]['json']), (('PATCH', '/bonfire/instances/prefs'), {'url': 'https://chat.ikelene.net', 'muted': True}))
            c.start_ember_import('discord', '1', ['2'], 'https://chat.example'); self.assertEqual(req.call_args[0], ('POST', '/bonfire/import'))
            c.ember_import_job('j1'); self.assertEqual(req.call_args[0], ('GET', '/bonfire/import/j1'))
            c.ember_payout('https://chat.ikelene.net'); self.assertEqual(req.call_args[1]['query'], {'url': 'https://chat.ikelene.net'})


if __name__ == '__main__':
    unittest.main()
