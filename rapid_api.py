import requests
import shutil
from datetime import datetime, timedelta
from youtube_upload import upload_video

# echochrimson@gmail.com
# 4am@G8g9v2%LMw
absolute_path = '/home/vector/vsCode/jigglypuff/'
today = datetime.now().date()
yesterday = today - timedelta(days=1)
with open('log.txt', 'w') as f:
    f.write(str(datetime.now()))

# Healine search, yt category, playlist id
cat_list = [['Global News', 'current events', 'PLPbMNnQbsm470OCS_BEpyBfUIaEp7OXLs'], ['Trending Entertainment', 'entertainment', 'PLPbMNnQbsm45zQrO_YJx8WdLHSZK6ZD7W'], 
            ['Trending Technology', 'technology', 'PLPbMNnQbsm45AZufdiRnjikkx8FZn5Lk8']]

#################################
# Search for top headlines
#################################
def get_news():
    ##################
    # REAL-TIME-NEWS
    ##################
    # url = 'https://real-time-news-data.p.rapidapi.com/top-headlines'
    url = 'https://real-time-news-data.p.rapidapi.com/search'
    querystring = {"query":item[0],"country":"US","lang":"en"}
    headers = {
        "X-RapidAPI-Key": "1a102fb261msh2d806b99ff6302ap13c953jsn29bf8eb677fe",       # Exceeded Quota
        "X-RapidAPI-Host": "real-time-news-data.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    resp_data = response.json()
    # with open('test.json', 'w') as f:
    #     f.write(response.text)

    try:
        # Save article and title info
        # print(resp_data)
        title = str(today) + '- ' + resp_data['data'][0]['title']
        article = resp_data['data'][0]['link']
        author = resp_data['data'][0]['author']
        return([title, article, author])
    except:
        print('Real-Time News error')
        with open('log.txt', 'w') as f:
            f.write('\nReal-Time News error')

    ##################
    # GOOGLE-NEWS
    ##################
    url = "https://google-news13.p.rapidapi.com/" + item[1]
    querystring = {"lr":"en-US"}
    headers = {
        "X-RapidAPI-Key": "1a102fb261msh2d806b99ff6302ap13c953jsn29bf8eb677fe",       # Other API Exceeded
        "X-RapidAPI-Host": "google-news13.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    resp_data = response.json()
    # print(resp_data)
    try:
        title = str(today) + '- ' + resp_data['items'][0]['title']
        article = resp_data['items'][0]['newsUrl']
        author = resp_data['items'][0]['publisher']
        return([title, article, author])
    except:
        print('\nGoogle News error')
        with open('log.txt', 'w') as f:
            f.write('\nGoogle News error')

    ##################
    # API-LAYER NEWS
    ##################
    url = "https://api.apilayer.com/world_news/search-news?text=" + item[1] + "&earliest-publish-date=" + str(yesterday) + "&source-countries=US,AU,CA,UK,NZ"
    print(url)
    payload = {}
    headers= {
    "apikey": "hkcLiwIF4sAC8CMJgAimff4pFDURRAY4"
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    result = response.json()

    with open('test.json', 'w') as f:
        f.write(response.text)
    try:
        title = str(today) + ': ' + item[0] + ", " + result['news'][0]['title']
        article = result['news'][0]['url']
        if('author' in result['news'][0]):
            author = result['news'][0]['author']
        else:
            author = 'Author Unknown'
        summary = result['news'][0]['summary']
        return([title, article, author])
    except:
        print('\nAPI-Layer News error')
        with open('log.txt', 'w') as f:
            f.write('\nAPI-Layer News error')
        return(['Error'])

###########################
# Summarize news article for description
###########################
def summarize(article):
    with open('log.txt', 'a') as f:
        f.write('\nSummarizing. . .')
    url = "https://article-extractor-and-summarizer.p.rapidapi.com/summarize"
    querystring = {"url": article,"length":"1"}
    headers = {
        "X-RapidAPI-Key": "1a102fb261msh2d806b99ff6302ap13c953jsn29bf8eb677fe",
        "X-RapidAPI-Host": "article-extractor-and-summarizer.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    resp_data = response.json()
    # print(resp_data)

    # If a summary is made save that as the video description, if not skip it
    try:
        description = resp_data['summary'] + '\nArticle Referenced: ' + article
    except:
        description = title + '\nArticle Referenced: ' + article
    return description

#################################
# Search for related TikTok
#################################
def get_tiktok(title, description):
    with open('log.txt', 'a') as f:
        f.write('\nSearching related tiktoks. . .')
    url = 'https://tiktok-scraper7.p.rapidapi.com/feed/search'
    querystring = {"keywords":title,"region":"us","count":"2","cursor":"0","publish_time":"0","sort_type":"0"}
    headers = {
        "X-RapidAPI-Key": "1a102fb261msh2d806b99ff6302ap13c953jsn29bf8eb677fe",
        "X-RapidAPI-Host": "tiktok-scraper7.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    tiktok_data = response.json()
    # print(tiktok_data)

    # Find a related tiktok and save the creator's name if it's there
    try:
        creator = "@" + tiktok_data['data']['videos'][0]['author']['unique_id'] + ' (' + tiktok_data['data']['videos'][0]['author']['nickname'] + ')'
    except:
        print('index out of range, skipping no creator')
        with open('log.txt', 'a') as f:
            f.write('\nindex out of range, skipping no creator')
    
    # Save the tiktok video as the category name if there's a response
    try:
        vid_name = item[0] + '.mp4'
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
        with open('\nlog.txt', 'a') as f:
            f.write('index out of range, skipping entire video')
        return(['Skipped'])

# Loop the 2D-Array searching for articles from General, Entertainment, and Tech categories then send them to youtube
for item in cat_list:
    with open('log.txt', 'a') as f:
        f.write('\nSearching news headlines. . .')
    print('Searching news headlines. . .')
    # Search 3 different APIs and return the title, link, and author of whichever one has a response
    news_resp = get_news()
    if(news_resp[0] != 'Error'):
        title = news_resp[0]
        article = news_resp[1]
        author = news_resp[2]

        with open('log.txt', 'a') as f:
            f.write('\nSummarizing. . .')
        print('Summarizing. . .')
        # Use the link from the headline found and summarize the article
        description = summarize(article)

        with open('log.txt', 'a') as f:
            f.write('\nSearching related tiktoks. . .')
        print('Searching related tiktoks. . .')
        # Find and save tiktok video based on the title, update the description with the creator info
        tiktok_resp = get_tiktok(title, description)
        if(len(tiktok_resp) > 1):
            description = tiktok_resp[0]
            vid_name = tiktok_resp[1]
            upload_video(title=title, description=description, category='technology', vid_name=vid_name, playlist_id=item[2])

    

    