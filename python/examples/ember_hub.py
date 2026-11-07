"""All the Ember servers saved on a Nookara account, with their joined communities.

    NOOKARA_TOKEN=... python bonfire_hub.py
"""
import os

from nookara import Ember, Client

nookara = Client(os.environ["NOOKARA_TOKEN"])
ember = Ember(nookara, sign="auto")
for item in ember.communities():
    community = item["community"]
    print(item["instance"], (community or {}).get("name", "-"), item["error"] or "")
