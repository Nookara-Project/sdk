"""Check the signatures of the latest messages yourself. Needs: pip install "velora-api-client[signing]"."""
import os

from velora_api import Client, Instance

chat = Instance("https://chat.ikelene.net")
chat.login_with_velora(Client(os.environ["VELORA_TOKEN"]))
for message in chat.messages(chat.channel_id("general"), limit=20)["messages"]:
    ok, reason = chat.verify_message(message)
    print(message["id"], "signed and valid" if ok else reason)
