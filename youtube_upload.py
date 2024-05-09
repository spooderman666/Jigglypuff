from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo


def upload_video(title, description, category, vid_name, playlist_id): 
    print('Uploading. . .')
    # loggin into the channel
    channel = Channel()
    channel.login(absolute_path + "client_secret.json", absolute_path + "storage_path")

    # setting up the video that is going to be uploaded
    video = LocalVideo(file_path = absolute_path + vid_name)

    # setting snippet
    if(len(title) > 100):
        title = title[0:90] + '...'
    video.set_title(title)
    video.set_description(description)
    video.set_tags([category])
    video.set_category(category)
    video.set_default_language("en-US")
    video.set_playlist(playlist_id)

    # setting status
    # video.set_embeddable(True)
    # video.set_license("creativeCommon")
    # video.set_privacy_status("private")
    # video.set_public_stats_viewable(True)

    # setting thumbnail
    # video.set_thumbnail_path('test_thumb.png')

    # uploading video and printing the results
    # try:
    #     video = channel.upload_video(video)
    #     # channel.add_video_to_playlist(video=video, playlist_id=playlist_id)
    #     print(video)
    # except:
    #     print('idk')
    try:
        video = channel.upload_video(video)
    except:
        print('playlist error')
        print(video)
    # channel.add_video_to_playlist(video=video, playlist_id=playlist_id)

    # liking video
    # video.like()