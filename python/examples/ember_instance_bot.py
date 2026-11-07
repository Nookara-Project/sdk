"""A bot on a Ember instance: answers "!ping" with "pong".

Create the bot in the instance (Server settings, Bots) or with Instance.create_bot(),
add it to the community, and keep its token private:

    BONFIRE_URL=https://chat.ikelene.net BONFIRE_BOT_TOKEN=... python bonfire_instance_bot.py
"""
import asyncio
import os

from nookara import Instance

bot = Instance(os.environ.get("BONFIRE_URL", "https://chat.ikelene.net"),
               bot_token=os.environ["BONFIRE_BOT_TOKEN"])


async def main():
    async with bot.bot_gateway() as gateway:
        async for event in gateway:
            if event["type"] != "MESSAGE_CREATE":
                continue
            message = event["data"]
            if message["content"].strip() == "!ping" and not message["author"].get("bot"):
                await asyncio.to_thread(bot.bot_send, message["channel_id"], "pong")


asyncio.run(main())
