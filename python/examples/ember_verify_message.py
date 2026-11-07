"""Check the signatures of the latest messages yourself. Needs: pip install "nookara[signing]"."""
import os

from nookara import Client, Instance

chat = Instance("https://chat.ikelene.net")
chat.login_with_nookara(Client(os.environ["NOOKARA_TOKEN"]))
for message in chat.messages(chat.channel_id("general"), limit=20)["messages"]:
    ok, reason = chat.verify_message(message)
    print(message["id"], "signed and valid" if ok else reason)
