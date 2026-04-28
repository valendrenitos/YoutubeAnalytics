import os
import csv
from datetime import datetime
from googleapiclient.discovery import build

API_KEY = os.getenv('YOUTUBE_API_KEY')

youtube = build('youtube', 'v3', developerKey=API_KEY)

def track_subscribers(channel_input: str, csv_file: str = "subscriber_history.csv"):
    try:
        if channel_input.startswith('@'):
            request = youtube.channels().list(
                part='snippet,statistics',
                forHandle=channel_input[1:]
            )
        else:
            request = youtube.channels().list(
                part='snippet,statistics',
                id=channel_input
            )
        
        response = request.execute()
        item = response['items'][0]

        subs = int(item['statistics']['subscriberCount'])
        channel_name = item['snippet']['title']
        today = datetime.now().strftime("%Y-%m-%d")

        file_exists = os.path.isfile(csv_file)
        
        with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['date', 'channel_name', 'channel_input', 'subscribers'])
            writer.writerow([today, channel_name, channel_input, subs])

        print(f"✓ [{today}] {channel_name:<30} → {subs:,} subscribers")
        return True

    except Exception as e:
        print(f"Failed to track {channel_input}: {e}")
        return False



if __name__ == "__main__":
    channels = [
        "@MrBeast",
        "@MrBeastGaming",
        "@PewDiePie",
        "@Markiplier",
        "@DudePerfect",

    ]

    print(" Starting YouTube Subscriber Tracker\n")
    success_count = 0
    
    for channel in channels:
        if track_subscribers(channel):
            success_count += 1
    
    print(f"\nDone! Tracked {success_count}/{len(channels)} channels successfully.")