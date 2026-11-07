"""Submit your bot to the Nookara bot gallery (Discovery > Bots) and check its review state.

    NOOKARA_TOKEN=... BOT_ID=258 python bot_gallery.py

The bot needs a description of at least 10 characters and an avatar first
(PATCH /chat/bots/:id and POST /chat/bots/:id/avatar, or the Ember bot settings).
"""
import os

from nookara import APIError, Client

nookara = Client(os.environ["NOOKARA_TOKEN"])
bot_id = os.environ["BOT_ID"]

nookara.save_gallery_listing(bot_id, long_description="Plays music in voice channels.",
                            tags=["music", "fun"], permissions=["send_messages"])
try:
    nookara.submit_to_gallery(bot_id)
except APIError as error:
    print("Not submitted:", error.error)

gallery = nookara.gallery_status(bot_id)["gallery"]
print(gallery["state"], gallery.get("review_message"))
