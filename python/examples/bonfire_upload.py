"""Upload a file and import a link, then post both. Needs the Upload Media scope.

    VELORA_TOKEN=... python bonfire_upload.py picture.png https://example.com/cat.png
"""
import os
import sys

from velora_api import Client, Instance, ScopeError

velora = Client(os.environ["VELORA_TOKEN"])
chat = Instance("https://chat.ikelene.net")
chat.login_with_velora(velora)
channel = chat.channel_id("general")
try:
    first = chat.upload(sys.argv[1], cid=channel)
    second = chat.import_media(sys.argv[2], cid=channel)
except ScopeError:
    raise SystemExit("Upload Media was not allowed on this sign-in. Log in again and keep it ticked.")
chat.send_message(channel, "Two pictures", attachments=[first, second])
