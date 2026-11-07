"""Send a signed message. Needs the optional extra: pip install "velora-api-client[signing]".

The token must hold Chat (2048) and Sign Messages (32768); the account signing key is
fetched from Nookara and kept in memory only.

    VELORA_TOKEN=... python bonfire_signed_message.py
"""
import os

from velora_api import Client, Instance

velora = Client(os.environ["VELORA_TOKEN"])
instance = Instance("https://chat.ikelene.net")
instance.login_with_velora(velora, sign=True)

sent = instance.send_message(instance.channel_id("general"), "Signed from Python")
print(sent["message"]["verified"])
instance.send_message(instance.channel_id("general"), "Unsigned on purpose", sign=False)
