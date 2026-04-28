import csv
from datetime import datetime
from googleapiclient.discovery import build

api_key = "YOUR_API_KEY"
youtube = build('youtube', 'v3', developerKey=api_key)

def track_subscribers(channel_input, csv_file="subscriber_history.csv"):
    # Get current subs
    if channel_input.startswith('@'):
        req = youtube.channels().list(part='statistics', forHandle=channel_input[1:])
    else:
        req = youtube.channels().list(part='statistics', id=channel_input)
    
    data = req.execute()
    subs = int(data['items'][0]['statistics']['subscriberCount'])
    channel_name = data['items'][0]['snippet']['title'] if 'snippet' in data['items'][0] else "Unknown"
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Append to CSV
    with open(csv_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([today, channel_name, channel_input, subs])
    
    print(f"[{today}] {channel_name}: {subs:,} subscribers")

# Run daily
track_subscribers("@MrBeast")