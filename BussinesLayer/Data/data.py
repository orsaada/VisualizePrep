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
