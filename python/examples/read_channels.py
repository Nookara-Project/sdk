"""List the channels of a Bonfire server.

    VELORA_TOKEN=... python read_channels.py https://chat.ikelene.net
"""
import os
import sys

from velora_api import Client, Instance

velora = Client(os.environ["VELORA_TOKEN"])
chat = Instance(sys.argv[1] if len(sys.argv) > 1 else "https://chat.ikelene.net")
chat.login_with_velora(velora)
for channel in chat.channels():
    print(channel["cid"], channel["name"], channel["type"])
