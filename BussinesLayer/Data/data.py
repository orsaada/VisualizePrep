import json


def extract_attribute(json_file_path, attr):
    json_file = open(json_file_path, encoding="utf-8")
    parsed_json = json.load(json_file)
    result = parsed_json["videos"][0]["insights"][attr]
    return result


def extract_actors(json_file_path):
    return extract_attribute(json_file_path, "faces")


def extract_emotions(json_file_path):
    return extract_attribute(json_file_path, "emotions")

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
