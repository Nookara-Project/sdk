"""Read the latest messages of a channel on a Bonfire instance (Nookara login).

    VELORA_TOKEN=... python bonfire_read_channel.py
"""
import os

from velora_api import Client, Instance

velora = Client(os.environ["VELORA_TOKEN"])
instance = Instance("https://chat.ikelene.net")
instance.login_with_velora(velora)

channel = instance.channel_id("#general")
for message in instance.messages(channel, limit=20)["messages"]:
    author = (message.get("author") or {}).get("username", "system")
    print(author + ":", message["body"])
