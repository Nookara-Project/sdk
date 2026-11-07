"""One bot token, every instance it is installed on (gallery installs included).

    VELORA_BOT_TOKEN=... python bonfire_bot_program.py
"""
import asyncio
import os

from velora_api import BotProgram


async def main():
    async with BotProgram(os.environ["VELORA_BOT_TOKEN"]) as bot:
        async for event in bot:
            if event["type"] == "MESSAGE_CREATE":
                message = event["data"]
                if message["content"].strip() == "!ping" and not message["author"].get("bot"):
                    await bot.send(event["instance"], message["channel_id"], "pong")
            elif event["type"] in ("instance_added", "instance_removed", "instance_error"):
                print(event["type"], event["instance"])


asyncio.run(main())
