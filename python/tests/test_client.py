import asyncio
import importlib
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
import threading
import unittest
from unittest.mock import patch

project_root = Path(__file__).parents[1]
sys.path.insert(0, str(project_root / 'python' if (project_root / 'python').is_dir() else project_root))
from nookara import APIError, Client, RealtimeClient, login
from nookara.client import OPERATIONS


class Handler(BaseHTTPRequestHandler):
    seen = []
    def log_message(self, *args):
        pass

    def do_GET(self):
        self.handle_request()
    do_POST = do_GET
    do_PUT = do_GET
    do_PATCH = do_GET
    do_DELETE = do_GET

    def handle_request(self):
        content = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        type(self).seen.append((self.command, self.path, dict(self.headers), content))
        if self.path == '/redirect':
            self.send_response(302)
            self.send_header('Location', '/must-not-follow')
            self.end_headers()
            return
        if self.path == '/limited':
            self.send_response(429)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Retry-After', '3')
            self.end_headers()
            self.wfile.write(b'{"error":"rate_limited"}')
            return
        self.send_response(204 if self.path == '/empty' else 200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        if self.path != '/empty':
            self.wfile.write(json.dumps({'ok':True, 'path':self.path}).encode())


class RestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1',0),Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f'http://127.0.0.1:{cls.server.server_port}'
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def client(self, **kwargs):
        return Client('dummy-secret',base_url=self.base,allow_insecure=True,**kwargs)

    def test_http_methods_encoding_json(self):
        c = self.client()
        c.put_storage_by_storageid_by_key(storageId='my app',key='a/b?#',json={'value':'雪'},query={'one':True,'skip':None,'many':[1,2]})
        method,path,headers,body = Handler.seen[-1]
        self.assertEqual(method,'PUT')
        self.assertEqual(path,'/storage/my%20app/a%2Fb%3F%23?one=true&many=1&many=2')
        self.assertEqual(json.loads(body),{'value':'雪'})
        self.assertEqual(headers['Authorization'],'Bearer dummy-secret')
        self.assertNotIn('dummy-secret',repr(c))

    def test_multipart_order_and_unicode(self):
        self.client().post_media_video_chunk(data={'sessionId':'test','chunkIndex':0,'totalChunks':1},files={'chunk':('video.webm',b'abc','video/webm')})
        body = Handler.seen[-1][3]
        self.assertLess(body.index(b'sessionId'),body.index(b'filename='))
        self.assertIn(b'Content-Type: video/webm',body)
        self.assertIn(b'abc\r\n--',body)

    def test_errors_empty_and_no_redirect(self):
        c = self.client()
        self.assertIsNone(c.request('DELETE','/empty'))
        with self.assertRaises(APIError) as ctx:
            c.request('GET','/limited')
        self.assertEqual((ctx.exception.status,ctx.exception.error,ctx.exception.retry_after),(429,'rate_limited',3))
        count = len(Handler.seen)
        with self.assertRaises(APIError): c.request('GET','/redirect')
        self.assertEqual(len(Handler.seen),count+1)

    def test_auth_modes_and_optional_path(self):
        c=self.client()
        c.get_chat_invite_by_code(code='test')
        self.assertNotIn('Authorization',Handler.seen[-1][2])
        c.delete_chat_presence_activity_by_key()
        self.assertEqual(Handler.seen[-1][1],'/chat/presence/activity')
        with self.assertRaises(ValueError): c.get_chat_api_v1_users_me()
        self.client(auth_scheme='Bot').get_chat_api_v1_users_me()
        self.assertEqual(Handler.seen[-1][2]['Authorization'],'Bot dummy-secret')
        c.post_chat_webhooks_by_wid_by_token(wid='w',token='secret',json={'content':'test'})
        self.assertNotIn('Authorization',Handler.seen[-1][2])

    def test_all_named_operations(self):
        for op,r in OPERATIONS.items():
            client=self.client(auth_scheme='Bot' if r['auth']=='bot' else 'Bearer')
            params={p['name']:'value /雪' for p in r['params']}
            with patch.object(client,'request',return_value='ok') as request:
                self.assertEqual(getattr(client,op)(**params),'ok')
                args,kw=request.call_args
                self.assertEqual(args[0],r['method'])
                self.assertNotIn(':',args[1])
                self.assertNotIn('雪',args[1])
                self.assertEqual(kw['auth'],r['auth'] in ('bearer','bot'))
        self.assertGreaterEqual(len(OPERATIONS),385)

    def test_invalid_parameters(self):
        c=self.client()
        for value in ['', '.', '..']:
            with self.assertRaises(ValueError): c.get_chat_servers_by_sid(sid=value)
        with self.assertRaises(TypeError): c.call('get_chat_servers_by_sid')
        with self.assertRaises(TypeError): c.call('get_chat_servers',unknown=1)
        with self.assertRaises(ValueError): c.request('GET','//evil.example')
        with self.assertRaises(ValueError): Client('secret',base_url='http://example.com')
        with self.assertRaises(ValueError): c.request('POST','/x',json={},files={})
        with self.assertRaises(ValueError): c.request('POST','/x',files={'file':('bad\r\nname',b'a','text/plain')})

    def test_convenience_payloads(self):
        c=self.client()
        with self.assertRaises(RuntimeError): c.send_dm('Tester','Hello')
        with patch.object(c,'post_chat_channels_by_cid_messages') as send:
            c.send_message('cid','Hello',reply_to='12')
            send.assert_called_once_with(cid='cid',json={'message':'Hello','reply_to':'12','attachments':[]})

    def test_login_flow_and_heartbeat_grace(self):
        module=importlib.import_module('nookara.client')
        with patch.object(module,'Client') as client, patch.object(module.time,'sleep'):
            client.return_value.post_auth_ext_code.return_value={'code':'code'}
            client.return_value.get_auth_ext_code_status.side_effect=[{'ready':False,'alive':False},{'ready':True,'token':'dummy'}]
            urls=[]
            self.assertEqual(login(scopes=2049, optional_scopes=16384, on_url=urls.append),'dummy')
            self.assertIn('/login?code=code&',urls[0])
            self.assertNotIn('dummy',urls[0])
            payload=client.return_value.post_auth_ext_code.call_args.kwargs['json']
            self.assertEqual(payload['permissions_integer'],(2049|16384)<<16)


    def test_gallery_helpers(self):
        c=self.client()
        with patch.object(c,'request',return_value={'ok':True}) as req:
            c.list_gallery('dj',tag='music',page=2); self.assertEqual(req.call_args[0],('GET','/bonfire/bots/gallery')); self.assertEqual(req.call_args[1]['query'],{'q':'dj','tag':'music','page':2})
            c.gallery_bot('258'); self.assertEqual(req.call_args[0],('GET','/bonfire/bots/gallery/258'))
            c.gallery_status('258'); self.assertEqual(req.call_args[0],('GET','/chat/bots/258/gallery'))
            c.submit_to_gallery('258',tags=['a1']); self.assertEqual(req.call_args[0],('POST','/chat/bots/258/gallery/submit')); self.assertEqual(req.call_args[1]['json'],{'tags':['a1']})
            c.save_gallery_listing('258',support_url='https://x.test'); self.assertEqual(req.call_args[0],('PUT','/chat/bots/258/gallery'))
            c.withdraw_from_gallery('258'); self.assertEqual(req.call_args[0],('POST','/chat/bots/258/gallery/withdraw'))
            c.gallery_ticket('258','https://chat.example'); self.assertEqual(req.call_args[0],('POST','/bonfire/bots/gallery/258/ticket')); self.assertEqual(req.call_args[1]['json'],{'instance':'https://chat.example'})

    def test_game_helpers(self):
        c=self.client()
        with patch.object(c,'request',return_value={'ok':True}) as req:
            c.game_status('cid1'); self.assertEqual(req.call_args[0],('GET','/chat/game/channels/cid1/status'))
            c.game_exec('cid1','list'); self.assertEqual(req.call_args[0],('POST','/chat/game/channels/cid1/console')); self.assertEqual(req.call_args[1]['json'],{'command':'list'})
            c.game_claim('sid1','cid1'); self.assertEqual(req.call_args[1]['json'],{'sid':'sid1','cid':'cid1'})
            c.game_unlink('sid1','g0123'); self.assertEqual(req.call_args[0],('DELETE','/chat/game/servers/sid1/instances/g0123'))
            c.game_unclaimed('sid1',q='mc'); self.assertEqual(req.call_args[1]['query']['q'],'mc')
            c.game_console('cid1',before=5); self.assertEqual(req.call_args[1]['query']['before'],5)

    def test_lookup_helpers(self):
        c=self.client()
        with patch.object(c,'request',return_value={'users':[{'username':'Ann'},{'username':'bo'}],'not_found':['x']}) as req:
            got=c.lookup_many(['Ann','bo','x','Ann',''])
            self.assertEqual(req.call_args[0],('GET','/account/lookup')); self.assertEqual(req.call_args[1]['query'],{'u':'Ann,bo,x'})
            self.assertEqual(sorted(got),['ann','bo'])
            c.lookup_many(['u%d'%i for i in range(150)]); self.assertEqual(req.call_count,3)
            self.assertEqual(req.call_args[1]['query']['u'].count(','),49)
            c.lookup('ann'); self.assertEqual(req.call_args[0],('GET','/account/lookup/ann'))
        with patch.object(c,'request',return_value={'members':[],'total':0,'next_offset':None}) as req:
            with self.assertWarns(DeprecationWarning): c.members('s0123456789',limit=50,offset=100)
            self.assertEqual(req.call_args[0],('GET','/chat/servers/s0123456789/members')); self.assertEqual(req.call_args[1]['query'],{'limit':50,'offset':100})
        self.assertEqual(OPERATIONS['post_account_lookup']['path'],'/account/lookup')

    def test_notification_helpers(self):
        c=self.client()
        with patch.object(c,'request',return_value={'unread':2,'categories':[]}) as req:
            c.notifications(unread=True,category='friends',limit=10); self.assertEqual(req.call_args[0],('GET','/account/notifications')); self.assertEqual(req.call_args[1]['query'],{'unread':1,'category':'friends','cursor':None,'limit':10})
            self.assertEqual(c.unread_notifications(),2); self.assertEqual(req.call_args[0],('GET','/account/notifications/unread-count'))
            c.mark_notifications_read([5,6]); self.assertEqual(req.call_args[0],('POST','/account/notifications/read')); self.assertEqual(req.call_args[1]['json'],{'ids':[5,6]})
            c.mark_notifications_read(all=True); self.assertEqual(req.call_args[1]['json'],{'all':True})
            c.mark_notifications_unread([5]); self.assertEqual(req.call_args[0],('POST','/account/notifications/unread'))
            c.delete_notification(5); self.assertEqual(req.call_args[0],('DELETE','/account/notifications/5'))
            self.assertEqual(c.notification_settings(),[]); self.assertEqual(req.call_args[0],('GET','/account/notification-settings'))
            c.set_notification_settings({'friends':{'email':False}}); self.assertEqual(req.call_args[0],('PATCH','/account/notification-settings')); self.assertEqual(req.call_args[1]['json'],{'prefs':{'friends':{'email':False}}})

class RealtimeTests(unittest.IsolatedAsyncioTestCase):
    async def test_auth_race_nonce_events_and_presence(self):
        from websockets.asyncio.server import serve
        seen=[]
        async def handler(ws):
            auth=json.loads(await ws.recv()); seen.append(auth)
            await asyncio.sleep(.03)
            await ws.send(json.dumps({'type':'auth_success','scopes':2048,'tos_required':False}))
            async for raw in ws:
                frame=json.loads(raw);seen.append(frame)
                if frame['type']=='chat_send':
                    await ws.send(json.dumps({'type':'chat_message','message':{'body':'event'}}))
                    await ws.send(json.dumps({'type':'chat_ack','nonce':frame['nonce'],'message':{'body':frame['message']}}))
        async with serve(handler,'127.0.0.1',0) as server:
            port=server.sockets[0].getsockname()[1]
            async with RealtimeClient('dummy',url=f'ws://127.0.0.1:{port}',allow_insecure=True) as chat:
                result=await chat.send_message('c','hello')
                self.assertEqual(result['type'],'chat_ack')
                self.assertEqual((await anext(chat))['type'],'chat_message')
                await chat.set_activity('App')
                await chat.clear_activity()
                await chat.watch_presence(['n%d'%i for i in range(250)])
                await asyncio.sleep(.02)
        self.assertEqual([x['type'] for x in seen],['auth_token','chat_hello','chat_send','set_rich_presence','clear_rich_presence','chat_presence_watch','chat_presence_watch'])
        self.assertEqual([len(x['usernames']) for x in seen if x['type']=='chat_presence_watch'],[200,50])

    async def test_auth_rejection_and_tos(self):
        from websockets.asyncio.server import serve
        for reply in [{'type':'auth_error','error':'invalid_token'}, {'type':'auth_success','tos_required':True,'scopes':2048}]:
            async def handler(ws):
                await ws.recv()
                await ws.send(json.dumps(reply))
                await ws.wait_closed()
            async with serve(handler,'127.0.0.1',0) as server:
                port=server.sockets[0].getsockname()[1]
                with self.assertRaises(APIError):
                    async with RealtimeClient('dummy',url=f'ws://127.0.0.1:{port}',allow_insecure=True): pass

    async def test_protocol_error_and_disconnect(self):
        from websockets.asyncio.server import serve
        async def handler(ws):
            await ws.recv()
            await ws.send('{"type":"auth_success","scopes":0}')
            frame=json.loads(await ws.recv())
            await ws.send(json.dumps({'type':'chat_error','nonce':frame['nonce'],'error':'not_allowed'}))
        async with serve(handler,'127.0.0.1',0) as server:
            port=server.sockets[0].getsockname()[1]
            async with RealtimeClient('dummy',url=f'ws://127.0.0.1:{port}',allow_insecure=True) as chat:
                with self.assertRaises(APIError) as ctx: await chat.send_message('c','test')
                self.assertEqual(ctx.exception.error,'not_allowed')
                with self.assertRaises(StopAsyncIteration): await anext(chat)


if __name__=='__main__': unittest.main()

class GameEventTests(unittest.IsolatedAsyncioTestCase):
    async def test_game_events_filter(self):
        from websockets.asyncio.server import serve
        async def handler(ws):
            await ws.recv()
            await ws.send(json.dumps({'type':'auth_success','scopes':2048,'tos_required':False}))
            await ws.send(json.dumps({'type':'chat_message','message':{}}))
            await ws.send(json.dumps({'type':'game_status','channel':'c','online':True}))
            await ws.send(json.dumps({'type':'game_console','channel':'c','lines':[]}))
            await asyncio.sleep(.3)
        async with serve(handler,'127.0.0.1',0) as server:
            port=server.sockets[0].getsockname()[1]
            async with RealtimeClient('dummy',url=f'ws://127.0.0.1:{port}',allow_insecure=True) as chat:
                got=[]
                async for frame in chat.game_events():
                    got.append(frame['type'])
                    if len(got)==2: break
        self.assertEqual(got,['game_status','game_console'])


class NotificationEventTests(unittest.IsolatedAsyncioTestCase):
    async def test_notification_events_filter(self):
        from websockets.asyncio.server import serve
        async def handler(ws):
            await ws.recv()
            await ws.send(json.dumps({'type':'auth_success','scopes':0,'tos_required':False}))
            await ws.send(json.dumps({'type':'im_received','message':{}}))
            await ws.send(json.dumps({'type':'notification_new','notification':{'id':1,'category':'friends'},'unread':1}))
            await ws.send(json.dumps({'type':'presence_update'}))
            await ws.send(json.dumps({'type':'notifications_updated','unread':0,'read':'all'}))
            await asyncio.sleep(.3)
        async with serve(handler,'127.0.0.1',0) as server:
            port=server.sockets[0].getsockname()[1]
            async with RealtimeClient('dummy',url=f'ws://127.0.0.1:{port}',allow_insecure=True) as chat:
                got=[]
                async for frame in chat.notification_events():
                    got.append(frame['type'])
                    if len(got)==2: break
        self.assertEqual(got,['notification_new','notifications_updated'])
