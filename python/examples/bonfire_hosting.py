"""Look at Nookara-hosted Bonfire servers you own (needs Chat; buying weeks needs Currency Pay)."""
import os

from velora_api import Client

velora = Client(os.environ["VELORA_TOKEN"])
for plan in velora.hosting_plans()["plans"]:
    print(plan["id"], plan["price_credits"], plan["period"])
for server in velora.hosting_servers()["servers"]:
    print(server["url"], server["plan"], server["billing"], server["paid_until"])
