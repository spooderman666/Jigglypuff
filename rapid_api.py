import requests
import random
import shutil
import logging
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

from youtube_upload import upload_video

# Set environment variables and global variables
load_dotenv()
YT_API_KEY = os.getenv('YT_ECHO_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
LOG_PATH = '/home/vector/vsCode/Jigglypuff/log_api.log'
logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
absolute_path = os.getenv('ABSOLUTE_PATH')
today = datetime.now().date()
hour = datetime.now().hour
yesterday = today - timedelta(days=1)
logger.info('New video upload bunch. . .')
    
# Use a random number generator to pick the topics to query
news_topics = ['&q=aliens', '&q=celebrity news',  '&q=stocks']
entertainment_topics = ['&q=jeopardy', '&q=BTS',  '&q=holidays']
tech_topics = ['&q=apple', '&q=tesla',  '&q=meta']
list = [0, 1, 2]
topic_index = random.choice(list)
news_topic = news_topics[topic_index]
entertainment_topic = entertainment_topics[topic_index]
tech_topic = tech_topics[topic_index]

global_query = f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}{news_topic}&country=au,ca,gb,us&category=politics,world,top&language=en"
entertainment_query = f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}{entertainment_topic}&country=us&category=entertainment&language=en"
tech_query = f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}{tech_topic}&country=au,ca,gb,us&category=science,technology&language=en"
# print(global_query)
# print(entertainment_query)
# print(tech_query)

# Healine search, yt category, playlist id
cat_list = [[25, 'PLPbMNnQbsm470OCS_BEpyBfUIaEp7OXLs', global_query], [24, 'PLPbMNnQbsm45zQrO_YJx8WdLHSZK6ZD7W', entertainment_query], 
            [28, 'PLPbMNnQbsm45AZufdiRnjikkx8FZn5Lk8', tech_query]]

#################################
# Search for top headlines
#################################
def get_news():
    ##################
    # NEWS_DATA
    ##################
    with open(LOG_PATH, 'a') as f:
        f.write('\n' + item[2])
    print(item[2])
    response = requests.get(item[2])
    result = response.json()
    # print(str(response.text))

    # with open('test.json', 'w') as f:
    #     f.write(response.text)
    try:
        title = str(today) + ': ' + result['results'][0]['title']
        article = result['results'][0]['link']
        # Save article author
        if('creator' in result['results'][0]):
            if(result['results'][0]['creator'] is None):
                author = 'Author Unknown'
            else:
                author = result['results'][0]['creator'][0]
        # Save keywords for video tags
        if('keywords' in result['results'][0]):
            if(result['results'][0]['keywords'] is None):
                tags = ['general']
            else:
                tags = result['results'][0]['keywords']
        else:
            author = 'Author Unknown'
        summary = result['results'][0]['description']

        with open(LOG_PATH, 'a') as f:
            f.write('\n' + title)
        return([title, article, author, tags, summary])
    except:
        print('\nNEWS_DATA error')
        with open(LOG_PATH, 'a') as f:
            f.write('\nNEWS_DATA error')
        return(['Error'])

###########################
# Summarize news article for description
###########################
def summarize(article, summary):
    logger.info('Summarizing. . .')
    # url = "https://article-extractor-and-summarizer.p.rapidapi.com/summarize"
    # querystring = {"url": article,"length":"1"}
    # headers = {
    #     "X-RapidAPI-Key": "1a102fb261msh2d806b99ff6302ap13c953jsn29bf8eb677fe",
    #     "X-RapidAPI-Host": "article-extractor-and-summarizer.p.rapidapi.com"
    # }
    # response = requests.get(url, headers=headers, params=querystring)
    # resp_data = response.json()
    # print(resp_data)

    # If a summary is made save that as the video description, if not skip it
    # try:
    #     description = resp_data['summary'] + '\nArticle Referenced: ' + article
    # except:
    if(summary != None):
        description = summary + '. Article Referenced: ' + article
    else:
        description = 'Article Referenced: ' + article
    return description

#################################
# Search for related TikTok
#################################
def get_tiktok(title, description):
    logger.info('Searching related tik toks. . .')
    url = "https://tiktok-video-no-watermark10.p.rapidapi.com/index/Tiktok/searchVideoListByKeywords"
    querystring = {"keywords":title,"cursor":"0","region":"US","publish_time":"1","count":"2","sort_type":"0"}
    headers = {
	"X-RapidAPI-Key": "1a102fb261msh2d806b99ff6302ap13c953jsn29bf8eb677fe",
	"X-RapidAPI-Host": "tiktok-video-no-watermark10.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    tiktok_data = response.json()
    # print(tiktok_data)

    # Find a related tiktok and save the creator's name if it's there
    try:
        creator = "@" + tiktok_data['data']['videos'][0]['author']['unique_id']
    except:
        print('index out of range, skipping no creator')
        logger.error('index out of range, skipping. . .')
    
    # Save the tiktok video as the category name if there's a response
    try:
        vid_name = 'to_upload.mp4'
        # print(tiktok_data['data']['videos'][0]['play'])
        r = requests.get(tiktok_data['data']['videos'][0]['play'], stream=True)
        if r.status_code == 200:
            with open(absolute_path + vid_name, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

        description = description + '\nContent Creator: ' + creator
        return([description, vid_name])
    except:
        print('index out of range, skipping entire video')
        logger.error('index out of range, skipping. . .')
        return(['Skipped'])

    ####################
    # Expired
    ####################
    # with open(LOG_PATH, 'a') as f:
    #     f.write('\nSearching related tiktoks. . .')
    # url = 'https://tiktok-scraper7.p.rapidapi.com/feed/search'
    # querystring = {"keywords":title,"region":"us","count":"2","cursor":"0","publish_time":"0","sort_type":"0"}
    # headers = {
    #     "X-RapidAPI-Key": "d599bf3470msh8e40da6c14c8729p19ea57jsn68278c03d12f",
    #     "X-RapidAPI-Host": "tiktok-scraper7.p.rapidapi.com"
    # }
    # response = requests.get(url, headers=headers, params=querystring)
    # tiktok_data = response.json()
    # # print(tiktok_data)

    # # Find a related tiktok and save the creator's name if it's there
    # try:
    #     creator = "@" + tiktok_data['data']['videos'][0]['author']['unique_id'] + ' (' + tiktok_data['data']['videos'][0]['author']['nickname'] + ')'
    # except:
    #     print('index out of range, skipping no creator')
    #     with open(LOG_PATH, 'a') as f:
    #         f.write('\nindex out of range, skipping no creator')
    
    # # Save the tiktok video as the category name if there's a response
    # try:
    #     # vid_name = item[0] + '.mp4'
    #     vid_name = 'to_upload.mp4'
    #     # print(tiktok_data['data']['videos'][0]['play'])
    #     r = requests.get(tiktok_data['data']['videos'][0]['play'], stream=True)
    #     if r.status_code == 200:
    #         with open(absolute_path + vid_name, 'wb') as f:
    #             r.raw.decode_content = True
    #             shutil.copyfileobj(r.raw, f)

    #     description = description + '\nContent Creator: ' + creator
    #     return([description, vid_name])
    # except:
    #     print('index out of range, skipping entire video')
    #     with open(LOG_PATH, 'a') as f:
    #         f.write('\nindex out of range, skipping entire video')
    #     return(['Skipped'])

# Loop the 2D-Array searching for articles from General, Entertainment, and Tech categories then send them to youtube
for item in cat_list:
    if(item[0] == 25):
        cat_name = "News & Politics"
        cat_id = item[0]
    elif(item[0] == 24):
        cat_name = "Entertainment"
        cat_id = item[0]
    elif(item[0] == 28):
        cat_name = "Science & Technology"
        cat_id = item[0]
    else:
        cat_name = item[0]
        cat_id = item[0]
    print('Searching news headlines. . .' + cat_name)
    logger.info('Searching news headlines. . .' + cat_name)

    # Search 3 different APIs and return the title, link, and author of whichever one has a response
    news_resp = get_news()
    if(news_resp[0] != 'Error'):
        title = news_resp[0]
        article = news_resp[1]
        author = news_resp[2]
        tags = news_resp[3]
        tags.append(cat_name)
        summary = news_resp[4]

        print('Summarizing. . .')
        # Use the link from the headline found and summarize the article
        description = summarize(article, summary)

        print('Searching related tiktoks. . .')
        # Find and save tiktok video based on the title, update the description with the creator info
        tiktok_resp = get_tiktok(title, description)
        print(title)
        print(description)
        if(len(tiktok_resp) > 1):
            description = tiktok_resp[0]
            # vid_name = tiktok_resp[1]
            vid_name = 'to_upload.mp4'
            upload_video(title=title, description=description, category=cat_id, vid_name=vid_name, playlist_id=item[1], tags=tags)