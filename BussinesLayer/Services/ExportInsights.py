from BussinesLayer.Algorithms.Visualize.mg.py3loader.experiment2_4 import extract_movie_results_to_json
from BussinesLayer.Algorithms.Visualize.mg.py3loader.algorithms_without_mg \
    import extract_movie_results_to_json_without_tt


def export_json_of_video_to_file(video_id, name):
    extract_movie_results_to_json(video_id, name)


def export_json_of_video_to_file_without_tt(video_id, name):
    extract_movie_results_to_json_without_tt(video_id, name)
