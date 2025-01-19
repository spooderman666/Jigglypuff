import os
import json
import requests
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv()
YT_API_KEY = os.getenv('YT_ME_API_KEY')
CHANNEL_ID='UCJ29pZWMjgqoG5uq9L6LWdw'

TECH_LIST = "PLPbMNnQbsm45sr3SmzqYKvDGExwW-_N9R"
ENTERTAIN_LIST = "PLPbMNnQbsm46lxMg8wfiJwniDuNGAkq4b"
GLOBAL_LIST = "PLPbMNnQbsm45AFpQZfSr5WmS6XEGWHTcM"
# TECH_LIST = "PLPbMNnQbsm45AZufdiRnjikkx8FZn5Lk8"
# ENTERTAIN_LIST = "PLPbMNnQbsm45zQrO_YJx8WdLHSZK6ZD7W"
# GLOBAL_LIST = "PLPbMNnQbsm470OCS_BEpyBfUIaEp7OXLs"
CATEGORY_MAP = {
    '24': ENTERTAIN_LIST,
    '25': GLOBAL_LIST,
    '28': TECH_LIST,
}

# Generate a temporary oauth token
def youtube_auth(): 
    client_secrets_file = 'client_secret.json'
    scope = ["https://www.googleapis.com/auth/youtube"] # The scope for accessing YouTube API
    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scope) # Create the flow using the client secrets file and the desired scope
    credentials = flow.run_local_server(port=8081)  # This opens a local server
    token = credentials.token  # This is the OAuth2 access token
    print(token)
    return token

# Add a video to a playlist based on id and stuff
def add_to_playlist(vid_id, play_id, token):
    header = {
        "Content-Type" : "application/json", 
        'Authorization': f'Bearer {token}'
        }
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet"
    body={
        'snippet': {
            'playlistId': play_id, 
            'resourceId': {
                    'kind': 'youtube#video',
                'videoId': vid_id
            }
        }
    }
    try:
        resp = requests.post(url=url,json=body, headers=header)
        print(resp.status_code)
        if(resp.status_code == 200):
            return True
        else:
            return False
    except:
        return False

token = youtube_auth()
# token = ""

# Function to get all videos from a playlist
def get_videos_from_playlist(playlist_id):
    playlist_videos = []
    next_page_token = None
    while True:
        if(next_page_token is not None):
            url = f"https://www.googleapis.com/youtube/v3/playlistItems?playlistId={playlist_id}&part=snippet&channelId={CHANNEL_ID}&key={YT_API_KEY}&pageToken={next_page_token}"
        else:
            url = f"https://www.googleapis.com/youtube/v3/playlistItems?playlistId={playlist_id}&part=snippet&channelId={CHANNEL_ID}&key={YT_API_KEY}"
        resp = requests.get(url)
        vid_list = json.loads(resp.text)
        # print(resp.text)

        # Iterate over the videos in the playlist
        for item in vid_list["items"]:
            video_id = item["snippet"]["resourceId"]["videoId"]
            video_title = item["snippet"]["title"]
            video_description = item["snippet"]["description"]
            playlist_videos.append(video_id)
            # playlist_videos.append({
            #     "videoId": video_id,
            #     "title": video_title,
            #     "description": video_description
            # })

        # Check if there's more pages, end the loop if needed
        if('nextPageToken' in vid_list):
            next_page_token = vid_list['nextPageToken']
        else:
            break
    return playlist_videos

# Get all video IDs from different playlists
print('Getting playlist videos. . .')
entertain_vids = get_videos_from_playlist(ENTERTAIN_LIST)
tech_vids = get_videos_from_playlist(TECH_LIST)
global_vids = get_videos_from_playlist(GLOBAL_LIST)

# Get all video IDs for the channel
channel_vids = []
next_page_token = None
while True:
    print('Getting channel videos. . .')
    if(next_page_token is not None):
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={CHANNEL_ID}&key={YT_API_KEY}&maxResults=1000&order=date&pageToken={next_page_token}"
    else:
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={CHANNEL_ID}&key={YT_API_KEY}&maxResults=1000&order=date"
    resp = requests.get(url)
    vid_list = json.loads(resp.text)

    # Make sure channel item is a video then save the IDs
    for item in vid_list["items"]:
        if(item['id']['kind'] == "youtube#video"):
            channel_vids.append(item['id']['videoId'])

    # Check if there's more pages, end the loop if needed
    if('nextPageToken' in vid_list):
        next_page_token = vid_list['nextPageToken']
    else:
        break

# Chunk the channel's video IDs in 10's 
cnt = 0
vid_set = []
all_vid_sets = []
for vid in channel_vids:
    if(cnt < 10):
        vid_set.append(vid)
    else:
        vid_set.append(vid)
        all_vid_sets.append(vid_set)
        cnt = 0
        vid_set = []
    cnt += 1

# Read each video id's data and add them to their playlists
for vid_set in all_vid_sets:
    id_text = ",".join(vid_set)
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={id_text}&key={YT_API_KEY}"
    resp = requests.get(url)
    id_resp = json.loads(resp.text)
    for item in id_resp['items']:
        print(item['id'])
        vid_id = item['id']
        if vid_id not in entertain_vids and vid_id not in tech_vids and vid_id not in global_vids:
            if(item['snippet']['categoryId'] == '24' or item['snippet']['categoryId'] == '25' or item['snippet']['categoryId'] == '28'):
                play_id = CATEGORY_MAP[item['snippet']['categoryId']]
                if(add_to_playlist(vid_id, play_id, token)):
                    print(f"{vid_id}: added to playlist")
                else:
                    print('fail')
        else:
            print("Already in playlist")