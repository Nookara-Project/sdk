"""All the Bonfire servers saved on a Nookara account, with their joined communities.

    VELORA_TOKEN=... python bonfire_hub.py
"""
import os

from velora_api import Bonfire, Client

velora = Client(os.environ["VELORA_TOKEN"])
bonfire = Bonfire(velora, sign="auto")
for item in bonfire.communities():
    community = item["community"]
    print(item["instance"], (community or {}).get("name", "-"), item["error"] or "")
