"""Look at Nookara-hosted Ember servers you own (needs Chat; buying weeks needs Currency Pay)."""
import os

from nookara import Client

nookara = Client(os.environ["NOOKARA_TOKEN"])
for plan in nookara.hosting_plans()["plans"]:
    print(plan["id"], plan["price_credits"], plan["period"])
for server in nookara.hosting_servers()["servers"]:
    print(server["url"], server["plan"], server["billing"], server["paid_until"])
