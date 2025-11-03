from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
import asyncio
import pandas as pd

# Your API credentials from https://my.telegram.org
API_ID = 'your_api_id'
API_HASH = 'your_api_hash'
PHONE_NUMBER = 'your_phone_number'

# Channel username (without @)
CHANNEL_USERNAME = 'channel_username'

async def scrape_channel_members():
    client = TelegramClient('session_name', API_ID, API_HASH)
    
    await client.start(PHONE_NUMBER)
    
    try:
        # Get the channel entity
        channel = await client.get_entity(CHANNEL_USERNAME)
        
        print(f"Scraping members from: {channel.title}")
        
        # Get participants
        participants = []
        offset = 0
        limit = 100
        
        while True:
            # Request participants in batches
            result = await client(GetParticipantsRequest(
                channel=channel,
                filter=ChannelParticipantsSearch(''),  # Empty string to get all
                offset=offset,
                limit=limit,
                hash=0
            ))
            
            if not result.participants:
                break
                
            for user in result.participants:
                participants.append({
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'phone': user.phone
                })
            
            offset += len(result.participants)
            print(f"Fetched {len(participants)} members so far...")
            
            # Telegram API rate limiting
            await asyncio.sleep(1)
            
            # Break if no more participants
            if len(result.participants) < limit:
                break
        
        # Save to CSV
        df = pd.DataFrame(participants)
        df.to_csv(f'{CHANNEL_USERNAME}_members.csv', index=False)
        print(f"Saved {len(participants)} members to CSV")
        
        return participants
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.disconnect()

# Run the scraper
if __name__ == "__main__":
    asyncio.run(scrape_channel_members())