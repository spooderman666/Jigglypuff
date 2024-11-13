from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium import webdriver
from dotenv import load_dotenv
import requests
import isodate
import random
import json
import time
import os

# Set environment variables and global variables
load_dotenv()
YT_API_KEY = os.getenv('YT_ME_API_KEY')
CHANNEL_ID='UCJ29pZWMjgqoG5uq9L6LWdw'
# DRIVER_PATH = 'dependencies/geckodriver'
# FIREFOX_PATH = 'dependencies/firefox'
DRIVER_PATH = '/usr/local/bin/geckodriver'
FIREFOX_PATH = '/usr/bin/firefox'
LOG_PATH = '/home/vector/vsCode/Jigglypuff/log_viewer.log'
with open(LOG_PATH, 'w') as f:
    f.write(str(datetime.now()))

###############################
# Get the length of a YT video based on its ID
###############################
def get_seconds(id):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={id}&key={YT_API_KEY}"
    resp = requests.get(url)
    yt_obj = json.loads(resp.text)
    duration = yt_obj['items'][0]['contentDetails']['duration']
    return int(isodate.parse_duration(duration).total_seconds())

#####################################
# Return a list of video IDs for Jigglypuff
#####################################
def get_ids():
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={CHANNEL_ID}&key={YT_API_KEY}&maxResults=50&order=date"
    resp = requests.get(url)
    video_resp = json.loads(resp.text)
    video_ids = []
 
    for item in video_resp['items']:
        video_ids.append(item['id']['videoId'])
    random.shuffle(video_ids)
    return video_ids

###############################################
# Read the list of videos to watch and watch them over a proxy
###############################################
video_ids = get_ids()
print('Retrieved youtube videos to view')
with open(LOG_PATH, 'a') as f:
    f.write('\nRetrieved youtube videos to view')

url = 'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all'
resp = requests.get(url)
file = open("proxies.txt", "w")
file.write(resp.text)
with open('proxies.txt', 'r') as file:
    proxies = [proxies.rstrip('\n') for proxies in file.readlines()]
file.close()
for proxy in proxies:
    # Set up Firefox and the driver for the new proxy
    service = Service(DRIVER_PATH)
    options = Options()
    options.binary_location = FIREFOX_PATH
    options.add_argument("--headless=new")
    options.add_argument("--websocket-port")
    options.add_argument(f"--proxy-server={proxy}")
    driver = webdriver.Firefox(service=service, options=options)
    print('Setup driver')
    with open(LOG_PATH, 'a') as f:
        f.write('\nSetup driver')

    # Get the videos
    for id in video_ids:
        video_url = f"https://youtu.be/{id}"
        secs = get_seconds(id)

        # Make sure there aren't issues hitting the play button
        try:
            # Open the YouTube video and let it load
            print('Loading: ' + id)
            with open(LOG_PATH, 'a') as f:
                f.write('\nLoading: ' + id)
            driver.get(video_url)
            time.sleep(1)

            # Find the play button to click
            print('Playing: ' + id)
            with open(LOG_PATH, 'a') as f:
                f.write('\nPlaying: ' + id)
            play_button = driver.find_element(By.CSS_SELECTOR, 'button.ytp-large-play-button')  # CSS Selector
            play_button.click()

            # Get the video ID to watch to duration and close the browser
            print('Watching: ' + id + ' for ' + str(secs))
            with open(LOG_PATH, 'a') as f:
                f.write('\nWatching: ' + id + ' for ' + str(secs))
        except ElementNotInteractableException:
            print("Element is not interactable, skipping")
        time.sleep(secs)
    driver.quit()