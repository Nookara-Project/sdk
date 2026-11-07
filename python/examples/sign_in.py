"""Ask the person to approve a token, then see what they actually allowed.

Scopes are requested, never required: the consent screen lets them untick any scope.
"""
from velora_api import Client, login, scope_mask

token = login(project_name="Example Python client", scopes=scope_mask("PROFILE_READ", "CHAT", "MEDIA_UPLOAD"))
velora = Client(token)
print("Allowed:", velora.scope_names())
if not velora.has_scope("CHAT"):
    raise SystemExit("Chat Messaging was not allowed: Bonfire servers need it. Run this again and keep it ticked.")
for entry in velora.bonfire_instances():
    print(entry["url"], "muted" if entry["muted"] else "")
