"""Read-only production checks of the installed wheel, never account mutations."""
import asyncio
import hashlib
from pathlib import Path
from velora_api import APIError, Client, Instance, RealtimeClient
from velora_api.client import OPERATIONS

root=Path(__file__).parents[1]
api=Client()
assert api.get_health()['status']=='ok'
assert api.get_chat_api_v1_gateway()['url'].startswith('wss://')
assert 'endpoints' in api.get_chat_api_discovery()
try:
    Client('velora-docs-deliberately-invalid-token').get_chat_servers()
except APIError as exc:
    assert exc.status==401
else:
    raise AssertionError('Invalid token unexpectedly accepted')
assert len(OPERATIONS)>=450
print('Installed wheel: %d operations; live health/discovery/gateway and invalid-token rejection passed'%len(OPERATIONS))
scopes=api.bonfire_scopes()
assert scopes and all(s['required'] is False for s in scopes)
assert api.bonfire_jwks()['keys']
assert 'results' in api.bonfire_directory()
assert 'results' in api.list_gallery()
assert api.server_latest()['build_id']
chat=Instance('https://chat.ikelene.net')
info=chat.discover()
assert info['software']=='bonfire-server' and info['accounts_mode'] in ('velora','local') and 'build' in info
assert chat.instance_info()['software']=='bonfire-server'
try:
    Client('velora-docs-deliberately-invalid-token').bonfire_session()
except APIError as exc:
    assert exc.status==401
print('Live Bonfire reads passed: scopes.json, JWKS, directory, gallery, server-latest, chat.ikelene.net discovery and info')

async def websocket_check():
    try:
        async with RealtimeClient('velora-docs-deliberately-invalid-token',timeout=15):
            raise AssertionError('Invalid websocket token accepted')
    except APIError as exc:
        assert exc.error=='invalid_token'
asyncio.run(websocket_check())
print('Live user websocket invalid-token rejection passed')

for relative in ['assets/css/shared-nav.css','assets/js/shared-nav.js','assets/js/accent.js','assets/icon.png']:
    destination=root/'build/preview-assets'/relative
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_bytes(api.request('GET','/'+relative,auth=False,raw=True))
print('Current public navigation assets ready for local preview')

from velora_api import BotClient, InvalidBotToken, __version__
assert __version__ == '0.5.9', __version__
try:
    BotClient('velora-docs-deliberately-invalid-token').list_payment_requests()
except InvalidBotToken as exc:
    assert exc.status == 401 and exc.error == 'invalid_bot_token'
else:
    raise AssertionError('Invalid bot token unexpectedly accepted')
print('Bot payments: invalid bot token rejected as InvalidBotToken (0.5.0)')
