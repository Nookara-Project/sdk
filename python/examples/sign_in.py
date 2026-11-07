"""Sign in through your registered app, then see what the person actually allowed.

Create the app in My Account > Apps with http://localhost as an authorized URL, and put its ID in NOOKARA_APP_ID.
The sign-in screen lets the person switch any scope off.
"""
import os

from nookara import Client, login_app

token, origin = login_app(os.environ["NOOKARA_APP_ID"])
nookara = Client(token, origin=origin)
print("Allowed:", nookara.scope_names())
if not nookara.has_scope("CHAT"):
    raise SystemExit("Chat wasn't allowed, and Ember servers need it. Sign in again and keep it on.")
for entry in nookara.ember_instances():
    print(entry["url"], "muted" if entry["muted"] else "")
