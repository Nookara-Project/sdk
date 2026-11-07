import asyncio
import os
from velora_api import RealtimeClient

async def main():
    async with RealtimeClient(os.environ['VELORA_TOKEN']) as chat:
        await chat.set_activity('Python example',state='Listening for messages')
        async for event in chat:
            if event.get('type')=='chat_message':
                print(event['message'])

asyncio.run(main())
