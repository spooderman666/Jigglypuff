import os
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo
from moviepy.editor import VideoFileClip, concatenate_videoclips

absolute_path = '/home/vector/vsCode/Jigglypuff/'

##################################################################
# Add trimmed Jigglypuff song to the end of videos
##################################################################
def merge_videos(vid_name):
    print('Adding Jigglypuff Song. . .')
    with open('/home/vector/vsCode/Jigglypuff/log.txt', 'a') as f:
        f.write('\nAdding Jigglypuff Song. . .')
    video_file_list = [absolute_path + vid_name, absolute_path + 'jiggle_song.mp4']
    loaded_video_list = []
    for video in video_file_list:
        print(f"Adding video file:{video}")
        loaded_video_list.append(VideoFileClip(video))
    final_clip = concatenate_videoclips(loaded_video_list, method='compose')
    merged_video_name = vid_name + '_merged'
    final_clip.write_videofile(absolute_path + f"{merged_video_name}.mp4")

##################################################################
# Upload to youtube
##################################################################
def upload_video(title, description, category, vid_name, playlist_id, tags): 
    merge_videos(vid_name=vid_name)
    print('Uploading. . .')
    with open('/home/vector/vsCode/Jigglypuff/log.txt', 'a') as f:
        f.write('\nUploading. . .')
    # loggin into the channel
    channel = Channel()
    channel.login(absolute_path + "client_secret.json", absolute_path + "storage_path")

    # setting up the video that is going to be uploaded
    video = LocalVideo(file_path = absolute_path + vid_name + '_merged.mp4')

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
        # print('playlist error')
        print(video)
        with open('/home/vector/vsCode/Jigglypuff/log.txt', 'a') as f:
            f.write('\nerror?')
    # channel.add_video_to_playlist(video=video, playlist_id=playlist_id)

    # liking video
    # video.like()

    # Remove all videos except jiggly
    with open('/home/vector/vsCode/Jigglypuff/log.txt', 'a') as f:
        f.write('\nCleaning. . .')
    files = os.listdir()
    for file in files:
        if(file.endswith('.mp4') and file != 'jiggle_song.mp4'):
            os.remove(file)