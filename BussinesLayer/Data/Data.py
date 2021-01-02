import json


def extract_attribute(json_file_path, attr):
    json_file = open(json_file_path, encoding="utf-8")
    parsed_json = json.load(json_file)
    result = parsed_json["videos"][0]["insights"][attr]
    return result


def extract_actors(json_file_path):
    json_file = open(json_file_path, encoding="utf-8")
    parsed_json = json.load(json_file)
    actors = parsed_json["videos"][0]["insights"]["faces"]
    return actors


def extract_emotions(json_file_path):
    json_file = open(json_file_path, encoding="utf-8")
    parsed_json = json.load(json_file)
    emotions = parsed_json["videos"][0]["insights"]["emotions"]
    return emotions


def get_actor_data(actors,actor_name):
    print("not implement yet")


def get_actor_appearances(actors,actor_name):
    print("not implement yet")


def get_specific_emotion_statistics(emotions,emotion_name):
    print("not implement yet")
