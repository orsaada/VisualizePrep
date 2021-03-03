from BussinesLayer.Algorithms.Visualize.mg.py3loader.experiment2_4 import extract_movie_results_to_json
from BussinesLayer.Services.APIconnection import get_info_json_from_video, export_json_to_file


def export_json_of_video_to_file(video_id, name):
    extract_movie_results_to_json(video_id, name)
