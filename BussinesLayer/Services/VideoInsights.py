# from BussinesLayer.Algorithms.Visualize.mg.py3loader.experiment2_4 import get_insight
from BussinesLayer.Services.APIconnection import upload_video, get_info_json_from_video
from DB.DB import add_new_video, get_my_movies, get_movieId


def load_video(path, future_name):
    return upload_video(path, future_name)  # return video id


def get_insights(video_id):
    return get_info_json_from_video(video_id)  # return json of info


def update_insights_in_db(username, movie_name, video_id):  # update db on a new analyzed video
    return add_new_video(username, movie_name, video_id)


def get_analyzed_data(tt_movie, json_path, alg):
    pass
    # return get_insight(tt_movie, json_path, alg)


def get_movie_id(username, name):
    return get_movieId(username,name)


def get_my_uploaded_videos(username):
    return get_my_movies(username)

