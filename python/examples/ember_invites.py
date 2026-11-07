"""Create a limited invite link, then list and remove it (needs Manage server on the instance)."""
import os

from nookara import Client, Instance

chat = Instance("https://chat.ikelene.net")
chat.login_with_nookara(Client(os.environ["NOOKARA_TOKEN"]))
invite = chat.create_invite(expires_in=3600, max_uses=5)
print("https://chat.ikelene.net/ invite code:", invite.get("code"))
print([i["code"] for i in chat.invites()])
chat.delete_invite(invite["code"])
