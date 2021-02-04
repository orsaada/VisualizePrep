from BussinesLayer.Services.APIconnection import upload_video, get_info_json_from_video
from DB.DB import add_new_video,get_my_movies


def load_video(path, future_name):
    return upload_video(path, future_name)  # return video id


def get_insights(video_id):
    return get_info_json_from_video(video_id)  # return json of info


def update_insights_in_db(username, video_id, path):  # update db on a new analyzed video
    return add_new_video(username, video_id, path)


def get_my_uploaded_videos(username):
    return get_my_movies(username)
