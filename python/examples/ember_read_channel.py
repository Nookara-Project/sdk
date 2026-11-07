"""Read the latest messages of a channel on a Ember instance (Nookara login).

    NOOKARA_TOKEN=... python bonfire_read_channel.py
"""
import os

from nookara import Client, Instance

nookara = Client(os.environ["NOOKARA_TOKEN"])
instance = Instance("https://chat.ikelene.net")
instance.login_with_nookara(nookara)

channel = instance.channel_id("#general")
for message in instance.messages(channel, limit=20)["messages"]:
    author = (message.get("author") or {}).get("username", "system")
    print(author + ":", message["body"])
