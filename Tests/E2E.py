import json
import os
import time

from video_indexer import VideoIndexer

from BussinesLayer.Algorithms.Visualize.mg.py3loader.split_movie import split_movie
from BussinesLayer.Data.data import extract_attribute, extract_speakers_list_from_transcript_data, \
    extract_speakers_list, extract_shots, manage_config
from Tests.utils import get_random_string, is_json
from BussinesLayer.Services.Login import log_in
from BussinesLayer.Services.Register import registration
from BussinesLayer.Services.APIconnection import upload_video, get_info_json_from_video, export_json_to_file
from BussinesLayer.Services.VideoInsights import get_analyzed_data, get_transcript_algo


def check_register_and_login_success():
    random_name = get_random_string(7)
    random_pass = get_random_string(7)
    if registration('1111', '1111', '1111', '1111', random_name, random_pass) == "Successfully Registration":
        if log_in(random_name, random_pass) == "Successfully Login":
            return 'pass'
        return 'failed'
    return 'failed'


def check_connection_video_indexer(vi):
    if vi is not None:
        return 'pass'
    else:
        return 'failed'


def check_upload_and_download_video_indexer():
    random_id = get_random_string(4)
    video_id = upload_video('./test_movie.mp4', f'test_movie_{random_id}')
    time.sleep(20)
    try:
        json_result = get_info_json_from_video(video_id)
        if is_json(f'"{json_result}"'):
            return 'pass'
        else:
            return 'failed'
    except:
        return 'failed'


def check_export_to_json():
    json_file = json.loads('{"test": "yes", "env": "dev", "kind": "E2E"}')
    random_id = get_random_string(4)
    try:
        export_json_to_file(json_file, f'test_{random_id}')
        return 'pass'
    except:
        return 'failed'


def check_algorithm_1():
    try:
        result1, result2 = get_analyzed_data('tt0037884', 'tt0037884', 1)
        if len(result1) != 0 and len(result2) != 0:
            return 'pass'
        else:
            return 'failed'
    except:
        return 'failed'


def check_algorithm_2():
    try:
        result1, result2 = get_analyzed_data('tt0037884', 'tt0037884', 2)
        if len(result1) != 0 and len(result2) != 0:
            return 'pass'
        else:
            return 'failed'
    except:
        return 'failed'


def check_algorithm_3():
    try:
        result1, result2 = get_analyzed_data('tt0037884', 'tt0037884', 3)
        if len(result1) != 0 and len(result2) != 0:
            return 'pass'
        else:
            return 'failed'
    except:
        return 'failed'


def check_algorithm_4():
    try:
        result1, result2 = get_analyzed_data('tt0037884', 'tt0037884', 4)
        if len(result1) != 0 and len(result2) != 0:
            return 'pass'
        else:
            return 'failed'
    except:
        return 'failed'


def check_extract_insights_data():
    file_path = manage_config()
    res1 = extract_attribute(file_path, 'topics')
    res2 = extract_attribute(file_path, 'brands')
    res3 = extract_attribute(file_path, 'faces')
    res4 = extract_attribute(file_path, 'namedLocations')
    res5 = extract_attribute(file_path, 'emotions')
    if len(res1) != 0 and len(res2) != 0 and len(res3) != 0 and len(res4) != 0 and len(res5) != 0:
        return 'pass'
    else:
        return 'failed'


def check_extract_transcript():
    file_path = manage_config()
    res1 = extract_speakers_list_from_transcript_data(file_path)
    res2 = extract_speakers_list(file_path)
    if len(res1) != 0 and len(res2) != 0:
        return 'pass'
    else:
        return 'failed'


def check_split_movie_and_action_recognition_and_clean_data_result():
    # need to replace in Or Saada computer
    res = split_movie('C:\\Users\\orel kakon\\Desktop\\VisualizePrep\\Tests\\test_movie.mp4', 'tt_test', 'test_movie')
    if len(res) != 0:
        return 'pass'
    else:
        return 'failed'


def check_extract_shots():
    file_path = manage_config()
    res = extract_shots(file_path)
    if len(res) != 0:
        return 'pass'
    else:
        return 'failed'


if __name__ == '__main__':
    CONFIG = {
        'SUBSCRIPTION_KEY': '05c4761dfdc04d899bb1c6eb6b98d882',
        'LOCATION': 'trial',
        'ACCOUNT_ID': '53ca1faf-9a1a-4951-a303-fd27f2f790a3'
    }
    vindexer = VideoIndexer(
        vi_subscription_key=CONFIG['SUBSCRIPTION_KEY'],
        vi_location=CONFIG['LOCATION'],
        vi_account_id=CONFIG['ACCOUNT_ID']
    )
    with open('./../config.json', 'r') as f:
        data = json.load(f)
    os.remove('./../config.json')
    with open('./../config.json', 'w') as f:
        data["UserLoggedIn"] = "aaaa"
        data["SpecificMoviePage"] = "FOUR_WEDDINGS_AND_ONE_FUNERAL_SCALED"
        data["ttMovie"] = "tt0109831"
        data["algo"] = ""
        data["ENV_MODE"] = 'production'
        json.dump(data, f, indent=4)
    test1 = check_register_and_login_success()
    test2 = check_connection_video_indexer(vindexer)
    test3 = check_upload_and_download_video_indexer()
    test4 = check_export_to_json()
    test5 = check_algorithm_1()
    test6 = check_algorithm_2()
    test7 = check_algorithm_3()
    test8 = check_algorithm_4()
    test9 = check_extract_insights_data()
    test10 = check_extract_transcript()
    test11 = check_extract_shots()
    test12 = check_split_movie_and_action_recognition_and_clean_data_result()
    print('TEST CASE 1 - check_register_and_login_success: ' + test1)
    print('TEST CASE 2 - check_connection_video_indexer: ' + test2)
    print('TEST CASE 3 - check_upload_and_download_video_indexer: ' + test3)
    print('TEST CASE 4 - check_export_to_json: ' + test4)
    print('TEST CASE 5 - check_algorithm_1: ' + test5)
    print('TEST CASE 6 - check_algorithm_2: ' + test6)
    print('TEST CASE 7 - check_algorithm_3: ' + test7)
    print('TEST CASE 8 - check_algorithm_4: ' + test8)
    print('TEST CASE 9 - check_extract_insights_data: ' + test9)
    print('TEST CASE 10 - check_extract_transcript: ' + test10)
    print('TEST CASE 11 - check_extract_shots: ' + test11)
    print('TEST CASE 12 - check_split_movie_and_action_recognition_and_clean_data_result: ' + test12)
