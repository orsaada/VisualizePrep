import json
import os
import datetime
from action_recognition import get_action_recognition
from analyze_action_data import get_clean_results


def try_parsing_date(text):
    for fmt in ('%H:%M:%S', '%H:%M:%S.%f'):
        try:
            return datetime.datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')


def generate_emotion_analysis(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
        scenes = []
        for i in data['videos'][0]['insights']['scenes']:
            scene = i['instances'][0]
            t = try_parsing_date(scene['start'])
            delta1 = datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
            t = try_parsing_date(scene['end'])
            delta2 = datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
            scenes.append((delta1, delta2))
        return scenes


def split_it(movie_path, json_path):
    file_path = movie_path
    scenes = generate_emotion_analysis(json_path)
    i = 1
    file_name = os.path.splitext(file_path)[0]
    file_name = os.path.basename(file_name)
    ROOT_DIR = os.path.abspath(os.curdir)
    path = os.path.join(ROOT_DIR, file_name)
    os.mkdir(path)
    for (start_time, end_time) in scenes:
        start_time = start_time
        end_time = end_time
        start_time_seconds = start_time.total_seconds()
        end_time_seconds = end_time.total_seconds()
        from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
        import math
        minutes = math.ceil((end_time_seconds - start_time_seconds) / 30)
        for j in range(minutes):
            interval = j * 30
            start_cut = start_time + datetime.timedelta(seconds=interval)
            if start_cut + datetime.timedelta(seconds=30) > end_time:
                end_cut = end_time
            else:
                end_cut = start_cut + datetime.timedelta(seconds=30)
            start_seconds = start_cut.total_seconds()
            end_seconds = end_cut.total_seconds()
            ffmpeg_extract_subclip(file_path, start_seconds, end_seconds, targetname=f"{path}/{i}.{j}.mp4")
        i += 1


# json_folder_path = "/Users/orsaada/university/FINAL PROJECT/visPrep/BussinesLayer/Algorithms/Visualize/vi_json"
# json_path = 'C:\\Users\\orel kakon\\Desktop' + '/' + 'tt_test.json'
# movies_folder_path = "/Users/orsaada/university/FINAL PROJECT/visPrep/BussinesLayer/Algorithms/Visualize/movies"
# movie_path = 'C:\\Users\\orel kakon\\Desktop' + '/' + 'test.mp4'


def split_movie(movie_path_from_load_movie, video_id_or_tt_movie, movie_name):
    root = os.path.abspath(os.curdir)
    json_path = f'{root}/../../vi_json/{video_id_or_tt_movie}.json'
    movie_path = movie_path_from_load_movie
    split_it(movie_path, json_path)
    get_action_recognition(f'./{movie_name}', movie_name)
    result = get_clean_results(f'{movie_name}.txt')
    return result


def remove_ir():
    import glob
    for i in glob.glob("*.mp4"):
        os.remove(i)

# remove_ir()

if __name__ == '__main__':
    # split_it('C:\\Users\\saada_z0zeuyu\\Desktop\\files\\test.mp4','C:\\Users\\saada_z0zeuyu\\Desktop\\files\\tt_test.json')
    s = split_movie('C:\\Users\\saada_z0zeuyu\\Desktop\\files\\test.mp4', 'tt_test', 'test')
    print(s)