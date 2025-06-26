#import necessary packages 
from googleapiclient.discovery import build
import pandas as pd
import time

# Add an API key from google cloud console
API_KEY = 'AIzaSyCLFFUShdw1qP6w4_S2x619qLIpIJcQHVs'

# Collect some working YouTube video ID's to work with 
video_ids = [
    'jNQXAC9IVRw',  # Me at the zoo
    'YoB8t0B4jx4',  # Mutant Giant Spider Dog
    '9bZkp7q19f0',  # Gangnam Style
    'kJQP7kiw5Fk',  # Despacito
    '3tmd-ClpJxA'   # Shape of You
]

# Initialize the API being used
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Create a way to get all the comments and replies using these ID's
def get_all_comments(video_id, max_pages=10):
    all_comments = []
    page_count = 0
    request = youtube.commentThreads().list(
        part='snippet,replies',
        videoId=video_id,
        textFormat='plainText',
        maxResults=100
    )

    while request and page_count < max_pages:
        response = request.execute()
        page_count += 1

        for item in response['items']:
            top = item['snippet']['topLevelComment']
            top_snippet = top['snippet']
            top_id = top['id']

            # Save top-level comment
            all_comments.append({
                'video_id': video_id,
                'comment_type': 'comment',
                'comment_id': top_id,
                'parent_id': None,
                'author': top_snippet.get('authorDisplayName'),
                'text': top_snippet.get('textDisplay')
            })

            # Save replies (if there are any)
            if 'replies' in item:
                for reply in item['replies']['comments']:
                    reply_snippet = reply['snippet']
                    all_comments.append({
                        'video_id': video_id,
                        'comment_type': 'reply',
                        'comment_id': reply['id'],
                        'parent_id': reply['snippet'].get('parentId'),
                        'author': reply_snippet.get('authorDisplayName'),
                        'text': reply_snippet.get('textDisplay')
                    })

        request = youtube.commentThreads().list_next(request, response)
        time.sleep(1)

    return all_comments

# put all the videos in a loop to get all the comments from each video
all_comments = []
for vid in video_ids:
    print(f"Fetching comments + replies for video: {vid}")
    try:
        comments = get_all_comments(vid, max_pages=5)
        all_comments.extend(comments)
    except Exception as e:
        print(f"Error with video {vid}: {e}")

# Save the information into a CSV file
df = pd.DataFrame(all_comments)
df.to_csv("youtube_comments_test.csv", index=False, encoding='utf-8')
print(f"Saved {len(df)} comments (including replies) to youtube_comments_with_replies.csv")
