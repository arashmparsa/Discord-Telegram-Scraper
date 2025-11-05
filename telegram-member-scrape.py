#!/usr/bin/env python3
"""
Telegram Channel Member Scraper - Official API Version
Uses Telethon with official Telegram API credentials
Only collects publicly available information
"""
from telethon import TelegramClient, errors
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch, ChannelParticipantsRecent
import asyncio
import pandas as pd
import os
import sys
from datetime import datetime
import json

# Configuration - Get API credentials from https://my.telegram.org
CONFIG = {
    'API_ID': os.getenv('TELEGRAM_API_ID', 'your_api_id'),
    'API_HASH': os.getenv('TELEGRAM_API_HASH', 'your_api_hash'),
    'PHONE': os.getenv('TELEGRAM_PHONE', 'your_phone_number'),
    'CHANNEL': os.getenv('TELEGRAM_CHANNEL', 'channel_username'),
    'SESSION_NAME': 'telegram_scraper_session',
    'BATCH_SIZE': 100,
    'RATE_LIMIT_DELAY': 2  # seconds between requests
}

async def scrape_channel_members():
    """Scrape members from a Telegram channel using official API"""

    print("=" * 60)
    print("TELEGRAM CHANNEL MEMBER SCRAPER")
    print("=" * 60)

    # Validate configuration
    if CONFIG['API_ID'] == 'your_api_id':
        print("\n[ERROR] API credentials not configured")
        print("\nSetup Instructions:")
        print("1. Go to https://my.telegram.org/apps")
        print("2. Log in with your phone number")
        print("3. Create a new application")
        print("4. Copy the API ID and API Hash")
        print("5. Set environment variables:")
        print("   export TELEGRAM_API_ID='your_api_id'")
        print("   export TELEGRAM_API_HASH='your_api_hash'")
        print("   export TELEGRAM_PHONE='+1234567890'")
        print("   export TELEGRAM_CHANNEL='channel_username'")
        sys.exit(1)

    # Initialize client
    client = TelegramClient(CONFIG['SESSION_NAME'],
                           int(CONFIG['API_ID']),
                           CONFIG['API_HASH'])

    try:
        print(f"\n[INFO] Connecting to Telegram...")
        await client.start(phone=CONFIG['PHONE'])
        print(f"[SUCCESS] Connected as {await client.get_me()}")

        # Get channel entity
        print(f"\n[INFO] Fetching channel: @{CONFIG['CHANNEL']}")
        channel = await client.get_entity(CONFIG['CHANNEL'])

        print(f"[SUCCESS] Found channel: {channel.title}")
        print(f"          Subscribers: ~{getattr(channel, 'participants_count', 'Unknown')}")

        # Scrape members
        participants = []
        offset = 0
        total_scraped = 0

        print(f"\n[INFO] Scraping members...")

        while True:
            try:
                # Request participants in batches
                result = await client(GetParticipantsRequest(
                    channel=channel,
                    filter=ChannelParticipantsRecent(),  # Get recent members
                    offset=offset,
                    limit=CONFIG['BATCH_SIZE'],
                    hash=0
                ))

                if not result.users:
                    print(f"\n[SUCCESS] No more members found")
                    break

                # Extract public information only
                for user in result.users:
                    member_data = {
                        'id': user.id,
                        'username': user.username if user.username else None,
                        'first_name': user.first_name if user.first_name else None,
                        'last_name': user.last_name if user.last_name else None,
                        'is_bot': user.bot if hasattr(user, 'bot') else False,
                        'is_premium': user.premium if hasattr(user, 'premium') else False,
                        'scraped_at': datetime.now().isoformat()
                    }
                    participants.append(member_data)

                total_scraped = len(participants)
                offset += len(result.users)

                print(f"   Fetched {total_scraped} members...", end='\r')

                # Rate limiting to respect Telegram's API limits
                await asyncio.sleep(CONFIG['RATE_LIMIT_DELAY'])

                # Break if we got fewer results than requested
                if len(result.users) < CONFIG['BATCH_SIZE']:
                    break

            except errors.FloodWaitError as e:
                print(f"\n[WARNING] Rate limited. Waiting {e.seconds} seconds...")
                await asyncio.sleep(e.seconds)
                continue

            except errors.ChatAdminRequiredError:
                print(f"\n[ERROR] Admin privileges required to access member list")
                print("        This channel's member list is private")
                break

        print(f"\n\n[SUCCESS] Scraped {len(participants)} members total")

        # Save to multiple formats
        if participants:
            # JSON format
            json_file = f'{CONFIG["CHANNEL"]}_members.json'
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(participants, f, indent=2, ensure_ascii=False)
            print(f"[SUCCESS] Saved to {json_file}")

            # CSV format
            df = pd.DataFrame(participants)
            csv_file = f'{CONFIG["CHANNEL"]}_members.csv'
            df.to_csv(csv_file, index=False, encoding='utf-8')
            print(f"[SUCCESS] Saved to {csv_file}")

            # Statistics
            print(f"\n[STATS] Statistics:")
            print(f"        Total members: {len(participants)}")
            print(f"        With usernames: {sum(1 for p in participants if p['username'])}")
            print(f"        Bots: {sum(1 for p in participants if p['is_bot'])}")
            print(f"        Premium users: {sum(1 for p in participants if p['is_premium'])}")

        return participants

    except errors.PhoneNumberInvalidError:
        print("\n[ERROR] Invalid phone number format")
        print("        Use international format: +1234567890")

    except errors.ApiIdInvalidError:
        print("\n[ERROR] Invalid API ID or API Hash")
        print("        Get valid credentials from https://my.telegram.org/apps")

    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

    finally:
        print(f"\n[INFO] Disconnecting...")
        await client.disconnect()
        print(f"[SUCCESS] Disconnected")

# Run the scraper
if __name__ == "__main__":
    asyncio.run(scrape_channel_members())