import json
from pathlib import Path
from time import mktime

import dateutil.parser
import pandas as pd
from PyQt5.QtChart import QBarSet

aaa = []


def check_attributes_exists(json_file_path):
    json_file = open(json_file_path, encoding="utf-8")
    parsed_json = json.load(json_file)
    for i in parsed_json["videos"][0]["insights"]:
        aaa.append(i)
    return aaa


def extract_attribute(json_file_path, attr):
    json_file = open(json_file_path, encoding="utf-8")
    parsed_json = json.load(json_file)
    try:
        result = parsed_json["videos"][0]["insights"][attr]
    except KeyError:
        result = []
    return result


def manage_config():
    base_path = Path(__file__).parent.parent.parent
    with open((base_path / 'config.json').resolve(), 'r') as f:
        data = json.load(f)
    movie_name = data["ttMovie"]
    movie_name = movie_name.replace(' ', '_')
    file_path = (base_path / "BussinesLayer/Algorithms/Visualize/vi_json/{}.json".format(movie_name)).resolve()
    return file_path


def extract_attribute_to_df(attr):
    file_path = manage_config()
    # print(file_path)
    attribute_json = extract_attribute(file_path, attr)
    # print(attribute_json)
    df = pd.DataFrame()
    for y in attribute_json:
        if not isinstance(y, str):
            df = df.append(y, ignore_index=True)
        else:
            pass
    return df


# def extract_attribute_to_df(json_file_path, attr):
#     attribute = extract_attribute(json_file_path, attr)
#     df1 = pd.DataFrame()
#     for y in attribute:
#         if not isinstance(y, str):
#             df1 = df1.append(y, ignore_index=True)
#         else:
#             pass
#     return df1


def extract_actors(json_file_path):
    return extract_attribute(json_file_path, "faces")


def extract_emotions(json_file_path):
    return extract_attribute(json_file_path, "emotions")


def extract_speakers(json_file_path):
    return extract_attribute(json_file_path, "speakers")


def extract_keywords(json_file_path):
    return extract_attribute(json_file_path, "keywords")


def extract_namedPeople(json_file_path):
    return extract_attribute(json_file_path, "namedPeople")


def extract_shots_or(json_file_path):
    return extract_attribute(json_file_path, "shots")


insights_array = []


def extract_all_data_to_csv(json_file_path):
    import json
    import pandas as pd

    path = ''
    json_file_path = "BussinesLayer/Algorithms/Visualize/vi_json/bad_santa.json"
    json_file = open(json_file_path, encoding="utf-8")
    parsed_json = json.load(json_file)
    df_array = {}
    result = parsed_json["videos"][0]["insights"]
    for x in result:
        category = parsed_json["videos"][0]["insights"][x]
        df = pd.DataFrame()
        for y in category:
            if not isinstance(y, str):
                df = df.append(y, ignore_index=True)
            else:
                pass
                # print(category)
                # print(y)

        df.to_csv(path + '{}.csv'.format(x))
        df_array[x] = df


#Nati
def extract_shots(json_file_path):
    json_file = open(json_file_path, encoding="utf-8")
    data = json.load(json_file)
    shots = []
    for i in data["videos"][0]["insights"]["shots"]:
        shots.append((i["instances"][0]["start"], i["instances"][0]["end"]))
    return shots


# Nati
def extract_speakers_list_from_transcript_data(json_file_path):
    json_file = open(json_file_path, encoding="utf-8")
    data = json.load(json_file)
    speakers = []
    for transcript_data in data["videos"][0]["insights"]["transcript"]:
        if transcript_data["text"] != "":
            speaker_name = "Speaker #"+ str(transcript_data["speakerId"])
            start = transcript_data["instances"][0]["start"]
            end = transcript_data["instances"][0]["end"]
            speakers.append((start,end,speaker_name))
        #else:
         #   print( transcript_data["text"])
    #print(sorted(speakers))
    return  sorted(speakers)
#extract_speakers_list_from_transcript_data("C:\\Users\\orel kakon\\Desktop\\תואר תכנה\\visualizeBGU2021\\27_dress_scaled.json")


# Nati
def extract_speakers_list(json_file_path):
    json_file = open(json_file_path, encoding="utf-8")
    data = json.load(json_file)
    speakers = []
    for speaker_instances_data in data["videos"][0]["insights"]["speakers"]:
        speaker_name = speaker_instances_data["name"]
        for sid in speaker_instances_data["instances"]:
            speakers.append((sid["start"],sid["end"],speaker_name))

    return sorted(speakers)


def get_actor_appearances(json_file_path, actor_name):
    faces = extract_actors(json_file_path)
    for face in faces:
        if face["name"] == actor_name:
            return face["instances"]


def get_specific_emotion_appearances(json_file_path, emotion_type):
    emotions = extract_emotions(json_file_path)
    for emotion in emotions:
        if emotion["name"] == emotion_type:
            return emotion["instances"]


def numpy_fix():
    pass


# transcript
def transcript(json_file_path):
    return extract_attribute(json_file_path, "transcript")
#
# # ocr
# def ocr():
#     pass
# # keywords
# def keywords():
#     pass
# # topics
# def topics():
#     pass
# # faces
# def faces():
#     pass
# # labels
# def labels():
#     pass
# # scenes
# def scenes():
#     pass
# # shots
# def shots():
#     pass
# # brands
# def brands():
#     pass
# # namedLocations
# def namedLocations():
#     pass
# # namedPeople
# def namedPeople():
#     pass
# # audioEffects
# def audioEffects():
#     pass
# # sentiments
# def sentiments():
#     pass
# # visualContentModeration
# def visualContentModeration():
#     pass
# # blocks
# def blocks():
#     pass
# # framePatterns
# def framePatterns():
#     pass
# # speakers
# def speakers():
#     pass
# # textualContentModeration
# def textualContentModeration():
#     pass
# # statistics
# def statistics():
#     pass

def format_time(str):
    return dateutil.parser.parse(str)
    # return datetime.strptime(str, "%H:%M:%S.%f")

def to_integer(dt_time):
    return 10000*dt_time.year + 100*dt_time.month + dt_time.day

def create_csvs():
    json_file_path = "../../BussinesLayer/Algorithms/Visualize/vi_json/27_dresses.json"
    json_file = open(json_file_path, encoding="utf-8")
    parsed_json = json.load(json_file)
    result = parsed_json["videos"][0]["insights"]
    for x in result:
        category = parsed_json["videos"][0]["insights"][x]
        df = pd.DataFrame()
        for y in category:
            if not isinstance(y, str):
                df = df.append(y, ignore_index=True)
        df.to_csv('{}.csv'.format(x))


def delete_csv():
    import os
    json_file_path = "../Algorithms/Visualize/vi_json/bad_santa.json"
    json_file = open(json_file_path, encoding="utf-8")
    parsed_json = json.load(json_file)
    result = parsed_json["videos"][0]["insights"]
    for x in result:
        os.remove("{}.csv".format(x))


def analyze_speakers_graph():
    df = extract_attribute_to_df("speakers")
    by_instance = pd.DataFrame(columns=['instance', 'start', 'end'])
    if df.empty:
        a, b = [], []
    else:
        a, b = df['instances'], df['name']
    for instances, name in zip(a, b):
        for y in instances:
            by_instance = by_instance.append({'instance': name, 'start': y['start'],
                                              'end': y['end']}, ignore_index=True)
    by_instance['start'] = pd.to_datetime(by_instance['start'])
    by_instance['end'] = pd.to_datetime(by_instance['end'])

    by_instance['range'] = by_instance['end'] - by_instance['start']
    by_instance = by_instance.groupby(['instance'])['range'].sum().reset_index(name='range')
    instances, ranges = list(by_instance['instance']), list(by_instance['range'])
    print(ranges)
    instances = list(map(lambda x: x.split()[1],instances))
    sets = []
    labelsX = []
    for ttype in instances:
        labelsX.append(ttype)
        sets.append(QBarSet(ttype))
    for i in range(len(ranges)):
        ranges[i] = ranges[i].total_seconds()
    return sets, ranges, labelsX


def analyze_emotions_graph():
    sets = []
    ranges = []
    file_path = manage_config()
    emotions = extract_emotions(file_path)
    all_emotions_list = ['Sad', 'Joy', 'Fear', 'Anger']
    for idx2, i in enumerate(emotions):
        if i['type'] in all_emotions_list:
            all_emotions_list.remove(i['type'])
        sets.append(QBarSet(i['type']))
        sum_time = 0
        for idx, val in enumerate(i['instances']):
            range_time = mktime(format_time(val['end']).timetuple()) - mktime(format_time(val['start']).timetuple())
            sum_time = sum_time + range_time
        ranges.append(sum_time)
    # if emotion missing add it with zero value
    for ttype in all_emotions_list:
        sets.append(QBarSet(ttype))
        ranges.append(0)
    return sets, ranges


def analyze_keywords_graph():
    file_path = manage_config()
    keywords = extract_keywords(file_path)
    df1 = pd.DataFrame()
    for y in keywords:
        if not isinstance(y, str):
            df1 = df1.append(y, ignore_index=True)
        else:
            pass
    number_of_instances = []
    for x in df1.instances:
        number_of_instances.append(len(x))
    df1['number_of_instances'] = number_of_instances
    langs = df1['text']  # ['C', 'C++', 'Java', 'Python', 'PHP']
    students = df1['number_of_instances']  # [23,17,35,29,12]
    return langs, students


if __name__ == '__main__':
    # json_str = "../../BussinesLayer/Algorithms/Visualize/vi_json/bad_santa.json"
    # json_file = open("../../BussinesLayer/Algorithms/Visualize/vi_json/bad_santa.json", encoding="utf-8")
    # parsed_json = json.load(json_file)
    # result = transcript(json_str)
    # data = {'row_1': [3, 2, 1, 0], 'row_2': ['a', 'b', 'c', 'd']}
    # df = pd.DataFrame()
    # for x in result:
    #     df = df.append(x, ignore_index=True)
    # print(df)
    # df.to_csv('transcript.csv')
    create_csvs()
    # delete_csv()


