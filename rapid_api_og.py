import requests
import shutil
from datetime import datetime, timedelta
from youtube_upload import upload_video

# echochrimson@gmail.com
# 4am@G8g9v2%LMw
news_api_key = 'hkcLiwIF4sAC8CMJgAimff4pFDURRAY4'
absolute_path = '/home/vector/vsCode/jigglypuff/'
today = datetime.now().date()
yesterday = today - timedelta(days=1)
with open('log.txt', 'w') as f:
    f.write(str(today))

# Healine search, yt category, playlist id
cat_list = [['Global News', 'general', 'PLPbMNnQbsm470OCS_BEpyBfUIaEp7OXLs'], ['Entertainment News', 'entertainment', 'PLPbMNnQbsm45zQrO_YJx8WdLHSZK6ZD7W'], 
            ['Trending Technology', 'technology', 'PLPbMNnQbsm45AZufdiRnjikkx8FZn5Lk8']]

for item in cat_list:
    #################################
    # Search for top headlines
    #################################
    # print('Searching news headlines. . .')
    # # url = 'https://real-time-news-data.p.rapidapi.com/top-headlines'
    # url = 'https://real-time-news-data.p.rapidapi.com/search'
    # querystring = {"query":item[0],"country":"US","lang":"en"}
    # headers = {
    #     "X-RapidAPI-Key": "1a102fb261msh2d806b99ff6302ap13c953jsn29bf8eb677fe",       # Exceeded Quota
    #     "X-RapidAPI-Host": "real-time-news-data.p.rapidapi.com"
    # }
    # response = requests.get(url, headers=headers, params=querystring)
    # resp_data = response.json()
    # # with open('test.json', 'w') as f:
    # #     f.write(response.text)

    # # Save article and title info
    # print(resp_data)
    # title = str(today) + '- ' + resp_data['data'][0]['title']
    # article = resp_data['data'][0]['link']
    # # print(title)

    # print('Searching headlines...')
    # url = "https://google-news13.p.rapidapi.com/" + item[1]
    # querystring = {"lr":"en-US"}
    # headers = {
    #     "X-RapidAPI-Key": "1a102fb261msh2d806b99ff6302ap13c953jsn29bf8eb677fe",       # Other API Exceeded
    #     "X-RapidAPI-Host": "google-news13.p.rapidapi.com"
    # }
    # response = requests.get(url, headers=headers, params=querystring)
    # resp_data = response.json()
    # print(resp_data)
    # title = str(today) + '- ' + resp_data['items'][0]['title']
    # author = resp_data['items'][0]['publisher']
    # article = resp_data['items'][0]['newsUrl']
    # print(article)

    # New API
    print('Searching news headlines. . .')
    with open('log.txt', 'a') as f:
        f.write('Searching news headlines. . .')
    url = "https://api.apilayer.com/world_news/search-news?text=" + item[1] + "&latest-publish-date=" + str(today) + "&earliest-publish-date=" + str(yesterday) + "&source-countries=US"
    payload = {}
    headers= {
    "apikey": "hkcLiwIF4sAC8CMJgAimff4pFDURRAY4"
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    status_code = response.status_code
    result = response.json()
    with open('test.json', 'w') as f:
        f.write(response.text)
    title = str(today) + ': ' + item[0] + ", " + result['news'][0]['title']
    article = result['news'][0]['url']
    author = result['news'][0]['author']
    print(title)
    # summary = result['news'][0]['summary']

    ###########################
    # Summarize news article for description
    ###########################
    print('Summarizing. . .')
    with open('log.txt', 'a') as f:
        f.write('Summarizing. . .')
    url = "https://article-extractor-and-summarizer.p.rapidapi.com/summarize"
    querystring = {"url": article,"length":"1"}
    headers = {
        "X-RapidAPI-Key": "1a102fb261msh2d806b99ff6302ap13c953jsn29bf8eb677fe",
        "X-RapidAPI-Host": "article-extractor-and-summarizer.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    resp_data = response.json()
    # print(resp_data)
    try:
        description = str(today) + '\n' + author + ':\n' + resp_data['summary'] + '\nArticle Referenced: ' + article
    except:
        description = str(today) + '\n' + author + ':\n' + title + '\nArticle Referenced: ' + article

    #################################
    # Search for related TikTok
    #################################
    print('Searching related tiktoks. . .')
    with open('log.txt', 'a') as f:
        f.write('Searching related tiktoks. . .')
    url = 'https://tiktok-scraper7.p.rapidapi.com/feed/search'
    querystring = {"keywords":title,"region":"us","count":"2","cursor":"0","publish_time":"0","sort_type":"0"}
    headers = {
        "X-RapidAPI-Key": "1a102fb261msh2d806b99ff6302ap13c953jsn29bf8eb677fe",
        "X-RapidAPI-Host": "tiktok-scraper7.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    tiktok_data = response.json()
    # print(tiktok_data)
    try:
        creator = "@" + tiktok_data['data']['videos'][0]['author']['unique_id'] + ' (' + tiktok_data['data']['videos'][0]['author']['nickname'] + ')'
    except:
        print('index out of range, skipping no creator')
        with open('log.txt', 'a') as f:
            f.write('index out of range, skipping no creator')
        
    try:
        # Save tiktok video
        vid_name = item[0] + '.mp4'
        print(tiktok_data['data']['videos'][0]['play'])
        r = requests.get(tiktok_data['data']['videos'][0]['play'], stream=True)
        if r.status_code == 200:
            with open(absolute_path + vid_name, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

        description = description + '\nContent Creator: ' + creator
        upload_video(title=title, description=description, category='technology', vid_name=vid_name, playlist_id=item[2])
        print(title)
        print(description)
    except:
        print('index out of range, skipping entire video')
        with open('log.txt', 'a') as f:
            f.write('index out of range, skipping entire video')
