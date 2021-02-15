import json
from pathlib import Path

import pandas as pd


def extract_attribute(json_file_path, attr):
    print(json_file_path)
    json_file = open(json_file_path, encoding="utf-8")
    parsed_json = json.load(json_file)
    result = parsed_json["videos"][0]["insights"][attr]
    return result

def get_attibute_json(attr):
    base_path = Path(__file__).parent.parent.parent
    with open((base_path / 'config.json').resolve(), 'r') as f:
        data = json.load(f)
    movie_name = data["SpecificMoviePage"]
    movie_name = movie_name.replace(' ', '_')
    file_path = (base_path / "BussinesLayer/Algorithms/Visualize/vi_json/{}.json".format(movie_name)).resolve()
    attribute_json = extract_attribute(file_path, attr)
    df = pd.DataFrame()
    for y in attribute_json:
        if not isinstance(y, str):
            df = df.append(y, ignore_index=True)
        else:
            pass
    return df

def extract_attribute_to_df(json_file_path, attr):
    attribute = extract_attribute(json_file_path, attr)
    df1 = pd.DataFrame()
    for y in attribute:
        if not isinstance(y, str):
            df1 = df1.append(y, ignore_index=True)
        else:
            pass
    return df1


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
    json_file_path = "BussinesLayer/Algorithms/Visualize/vi_json/27_DRESSES_SCALED.json"
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
#Nati
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

#Nati
def extract_speakers_list(json_file_path):
    json_file = open(json_file_path, encoding="utf-8")
    data = json.load(json_file)
    speakers = []
    for speaker_instances_data in data["videos"][0]["insights"]["speakers"]:
        speaker_name = speaker_instances_data["name"]
        for sid in speaker_instances_data["instances"]:
            speakers.append((sid["start"],sid["end"],speaker_name))

    return  sorted(speakers)

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

# ocr
def ocr():
    pass
# keywords
def keywords():
    pass
# topics
def topics():
    pass
# faces
def faces():
    pass
# labels
def labels():
    pass
# scenes
def scenes():
    pass
# shots
def shots():
    pass
# brands
def brands():
    pass
# namedLocations
def namedLocations():
    pass
# namedPeople
def namedPeople():
    pass
# audioEffects
def audioEffects():
    pass
# sentiments
def sentiments():
    pass
# visualContentModeration
def visualContentModeration():
    pass
# blocks
def blocks():
    pass
# framePatterns
def framePatterns():
    pass
# speakers
def speakers():
    pass
# textualContentModeration
def textualContentModeration():
    pass
# statistics
def statistics():
    pass

def create_csvs():
    json_file_path = "../../BussinesLayer/Algorithms/Visualize/vi_json/27_DRESSES_SCALED.json"
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
    json_file_path = "../../BussinesLayer/Algorithms/Visualize/vi_json/27_DRESSES_SCALED.json"
    json_file = open(json_file_path, encoding="utf-8")
    parsed_json = json.load(json_file)
    result = parsed_json["videos"][0]["insights"]
    for x in result:
      os.remove("{}.csv".format(x))



#try
if __name__ == '__main__':
    # json_str = "../../BussinesLayer/Algorithms/Visualize/vi_json/27_DRESSES_SCALED.json"
    # json_file = open("../../BussinesLayer/Algorithms/Visualize/vi_json/27_DRESSES_SCALED.json", encoding="utf-8")
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


