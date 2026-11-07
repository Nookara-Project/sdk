import asyncio
import os
from nookara import RealtimeClient

async def main():
    async with RealtimeClient(os.environ['NOOKARA_TOKEN']) as chat:
        await chat.set_activity('Python example',state='Listening for messages')
        async for event in chat:
            if event.get('type')=='chat_message':
                print(event['message'])

asyncio.run(main())
