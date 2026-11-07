"""List the channels of a Ember server.

    NOOKARA_TOKEN=... python read_channels.py https://chat.ikelene.net
"""
import os
import sys

from nookara import Client, Instance

nookara = Client(os.environ["NOOKARA_TOKEN"])
chat = Instance(sys.argv[1] if len(sys.argv) > 1 else "https://chat.ikelene.net")
chat.login_with_nookara(nookara)
for channel in chat.channels():
    print(channel["cid"], channel["name"], channel["type"])
