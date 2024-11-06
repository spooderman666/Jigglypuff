from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from dotenv import load_dotenv
import requests
import random
import json
import time
import os

# Set environment variables and global variables
load_dotenv()
KEY = os.getenv('KEY')
CHANNEL_ID='UCJ29pZWMjgqoG5uq9L6LWdw'
# DRIVER_PATH = 'dependencies/geckodriver'
# FIREFOX_PATH = 'dependencies/firefox'
DRIVER_PATH = '/usr/local/bin/geckodriver'
FIREFOX_PATH = '/usr/bin/firefox'
PROXY = "138.197.148.215:80"

#####################################
# Return a list of video IDs for Jigglypuff
#####################################
def get_ids():
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={CHANNEL_ID}&key={KEY}&maxResults=50&order=date"
    resp = requests.get(url)
    video_resp = json.loads(resp.text)
    video_ids = []
 
    for item in video_resp['items']:
        video_ids.append(item['id']['videoId'])
    random.shuffle(video_ids)
    return video_ids

# Set up Firefox and the driver
service = Service(DRIVER_PATH)
options = Options()
options.binary_location = FIREFOX_PATH
options.add_argument("--headless=new")
options.add_argument("--websocket-port")
options.add_argument(f"--proxy-server={PROXY}")
driver = webdriver.Firefox(service=service, options=options)
print('Setup driver')

# Iterate videos from Jigglypuff's news to watch
video_ids = get_ids()
print('Retrieved youtube videos to view')
for id in video_ids:
    video_url = f"https://youtu.be/{id}"

    # Open the YouTube video and let it load
    print('Loading: ' + id)
    driver.get(video_url)
    time.sleep(1)

    # Find the play button to click
    print('Playing: ' + id)
    play_button = driver.find_element(By.CSS_SELECTOR, 'button.ytp-large-play-button')  # CSS Selector
    play_button.click()

    # Watch the video and close the browser
    print('Watching: ' + id)
    time.sleep(31)
driver.quit()