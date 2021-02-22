# import json
# import pandas as pd
# # attr - keywords(most talked), faces, emotions .....
# def extract_attribute(json_file_path, attr):
#     json_file = open(json_file_path, encoding="utf-8")
#     parsed_json = json.load(json_file)
#     result = parsed_json["videos"][0]["insights"][attr]
#     return result
#
#
# def extract_actors(json_file_path):
#     return extract_attribute(json_file_path, "faces")
#
#
# def extract_emotions(json_file_path):
#     return extract_attribute(json_file_path, "emotions")
#
#
# def get_actor_appearances(json_file_path, actor_name):
#     faces = extract_actors(json_file_path)
#     for face in faces:
#         if face["name"] == actor_name:
#             return face["instances"]
#
#
# def get_specific_emotion_appearances(json_file_path, emotion_type):
#     emotions = extract_emotions(json_file_path)
#     for emotion in emotions:
#         if emotion["name"] == emotion_type:
#             return emotion["instances"]
#
# def numpy_fix():
#     pass
#
#
# # transcript
# def transcript(json_file_path):
#     return extract_attribute(json_file_path, "transcript")
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
#
# def create_csvs():
#     json_file_path = "../../BussinesLayer/Algorithms/Visualize/vi_json/bad_santa.json"
#     json_file = open(json_file_path, encoding="utf-8")
#     parsed_json = json.load(json_file)
#     result = parsed_json["videos"][0]["insights"]
#     for x in result:
#         category = parsed_json["videos"][0]["insights"][x]
#         df = pd.DataFrame()
#         for y in category:
#             if not isinstance(y, str):
#                 df = df.append(y, ignore_index=True)
#         df.to_csv('{}.csv'.format(x))
# # os.remove("/tmp/<file_name>.txt")
#
# def delete_csv():
#     import os
#     json_file_path = "../../BussinesLayer/Algorithms/Visualize/vi_json/bad_santa.json"
#     json_file = open(json_file_path, encoding="utf-8")
#     parsed_json = json.load(json_file)
#     result = parsed_json["videos"][0]["insights"]
#     for x in result:
#       os.remove("{}.csv".format(x))
#
#
#
# #try
# if __name__ == '__main__':
#     # json_str = "../../BussinesLayer/Algorithms/Visualize/vi_json/bad_santa.json"
#     # json_file = open("../../BussinesLayer/Algorithms/Visualize/vi_json/bad_santa.json", encoding="utf-8")
#     # parsed_json = json.load(json_file)
#     # result = transcript(json_str)
#     # data = {'row_1': [3, 2, 1, 0], 'row_2': ['a', 'b', 'c', 'd']}
#     # df = pd.DataFrame()
#     # for x in result:
#     #     df = df.append(x, ignore_index=True)
#     # print(df)
#     # df.to_csv('transcript.csv')
#     create_csvs()
#     delete_csv()
#
#
