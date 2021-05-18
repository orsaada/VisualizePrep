import json
import os

from moviepy.editor import VideoFileClip

import datetime

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

json_folder_path = "/Users/orsaada/university/FINAL PROJECT/visPrep/BussinesLayer/Algorithms/Visualize/vi_json"
json_path = json_folder_path + '/tt0037884.json'
movies_folder_path = "/Users/orsaada/university/FINAL PROJECT/visPrep/BussinesLayer/Algorithms/Visualize/movies"
movie_path = movies_folder_path + '/THE_LOST_WEEKEND_SCALED.mp4'


def try_parsing_date(text):
    print(text)
    for fmt in ('%H:%M:%S', '%H:%M:%S.%f'):
        try:
            return datetime.datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')


def generate_emotion_analysis():
    with open(json_path, 'r') as f:
        data = json.load(f)
        scenes = []
        for i in data['videos'][0]['insights']['scenes']:
            scene = i['instances'][0]
            # print(scene['start'])
            t = try_parsing_date(scene['start'])
            delta1 = datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
            # print(delta1)
            t = try_parsing_date(scene['end'])
            delta2 = datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
            scenes.append((delta1, delta2))
            # date_time_obj = datetime.datetime.strptime(date_time_str, '%b %d %Y %I:%M%p')

        # print(len(scenes))
        return scenes


def split_it():
    # file_path = "/Users/orsaada/university/FINAL PROJECT/2.mp4"
    file_path = movie_path
    # scenes = [(datetime.timedelta(0), datetime.timedelta(seconds=394, microseconds=461000)),
    #           (datetime.timedelta(seconds=394, microseconds=461000),
    #            datetime.timedelta(seconds=613, microseconds=913000))]
    scenes = generate_emotion_analysis()
    i = 1
    from pathlib import Path
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
        print(f"scene {i}")
        print(f"minutes {minutes}")
        # start_cut = start_time
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


split_it()


def remove_ir():
    import glob
    for i in glob.glob("*.mp4"):
        os.remove(i)

# remove_ir()
