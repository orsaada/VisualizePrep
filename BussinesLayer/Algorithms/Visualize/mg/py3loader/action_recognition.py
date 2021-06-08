import pandas as pd
from absl import logging
import tensorflow as tf
import tensorflow_hub as hub
import re
import tempfile
import ssl
import cv2
import numpy as np
import os
import math as Math
# import imageio
from urllib import request  # requires python3


def list_ucf_videos(UCF_ROOT, unverified_context):
    global _VIDEO_LIST
    if not _VIDEO_LIST:
        index = request.urlopen(UCF_ROOT, context=unverified_context).read().decode("utf-8")
        videos = re.findall("(v_[\w_]+\.avi)", index)
        _VIDEO_LIST = sorted(set(videos))
    return list(_VIDEO_LIST)


# def fetch_ucf_video(video, _CACHE_DIR, UCF_ROOT, unverified_context):
#     """Fetchs a video and cache into local filesystem."""
#     cache_path = os.path.join(_CACHE_DIR, video)
#     if not os.path.exists(cache_path):
#         urlpath = request.urljoin(UCF_ROOT, video)
#         data = request.urlopen(urlpath, context=unverified_context).read()
#         open(cache_path, "wb").write(data)
#     return cache_path


# Utilities to open video files using CV2
def crop_center_square(frame):
    y, x = frame.shape[0:2]
    min_dim = min(y, x)
    start_x = (x // 2) - (min_dim // 2)
    start_y = (y // 2) - (min_dim // 2)
    return frame[start_y:start_y+min_dim,start_x:start_x+min_dim]


def load_video(path, max_frames=0, resize=(224, 224)):
    cap = cv2.VideoCapture(path)
    frames = []
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = crop_center_square(frame)
            frame = cv2.resize(frame, resize)
            frame = frame[:, :, [2, 1, 0]]
            frames.append(frame)

            if len(frames) == max_frames:
                break
    finally:
        cap.release()
    return np.array(frames) / 255.0


def predict(sample_video, i3d, labels):
    model_input = tf.constant(sample_video, dtype=tf.float32)[tf.newaxis, ...]

    logits = i3d(model_input)['default'][0]
    probabilities = tf.nn.softmax(logits)

    # print("Top 5 actions:")
    prediction_small_video = []
    for i in np.argsort(probabilities)[::-1][:5]:
        prediction_small_video.append(f"  {labels[i]:22}: {probabilities[i] * 100:5.2f}%\n")
        # print(f"  {labels[i]:22}: {probabilities[i] * 100:5.2f}%")
    return prediction_small_video


def get_action_recognition(movie_path, movie_name):
    logging.set_verbosity(logging.ERROR)
    data_path = movie_path  # need to check relative !!!!!
    UCF_ROOT = "https://www.crcv.ucf.edu/THUMOS14/UCF101/UCF101/"
    global _VIDEO_LIST
    _VIDEO_LIST = None
    unverified_context = ssl._create_unverified_context()

    # @title Get the kinetics-400 labels
    # Get the kinetics-400 action labels from the GitHub repository.
    KINETICS_URL = "https://raw.githubusercontent.com/deepmind/kinetics-i3d/master/data/label_map.txt"
    with request.urlopen(KINETICS_URL) as obj:
        labels = [line.decode("utf-8").strip() for line in obj.readlines()]

    """# Using the UCF101 dataset"""

    # Get the list of videos in the dataset.
    ucf_videos = list_ucf_videos(UCF_ROOT, unverified_context)

    categories = {}
    for video in ucf_videos:
        category = video[2:-12]
        if category not in categories:
            categories[category] = []
        categories[category].append(video)

        for category, sequences in categories.items():
            summary = ", ".join(sequences[:2])
            print("%-20s %4d videos (%s, ...)" % (category, len(sequences), summary))

    i3d = hub.load("https://tfhub.dev/deepmind/i3d-kinetics-400/1").signatures['default']

    arr = []
    for filename in os.listdir(data_path):
        if filename.endswith(".mp4"):
            arr.append(filename)
    arr.sort(key=lambda x: float(x[:-4]))

    with open(f'{movie_name}.txt', 'a') as the_file:
        for indexi in arr:
            ss = load_video(data_path + '/' + indexi)
            scene_number = Math.floor(float(indexi.split('.')[0]))
            the_file.write(str(scene_number) + '\n')
            res_predict = predict(ss, i3d, labels)
            for line in res_predict:
              the_file.write(line)
            if indexi == 2:
                break


#
# # Sad Joy Fear Anger
# # {'Angry': 0.12, 'Fear': 0.42, 'Happy': 0.04, 'Sad': 0.33, 'Surprise': 0.08}
#
# # !pip install text2emotion
# import text2emotion as te
# texts = []
# scene_emotion_prediction = []
# for scene in results_array:
#   emotion_scene = {'Angry': 0, 'Fear': 0, 'Happy': 0, 'Sad': 0, 'Surprise': 0}
#   for scene_section in scene:
#     # all_mini_scenes.append([scene_section[0]])
#     print(scene_section[0])
#     scene_section_emotion = te.get_emotion(scene_section[0])
#     print(scene_section_emotion)
#     emotion_scene = {k: emotion_scene.get(k, 0) + scene_section_emotion.get(k, 0) for k in set(emotion_scene)}
#   scene_emotion_prediction.append(emotion_scene)
#
#
#
# df = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'))
# print(df)
#
# print(scene_emotion_prediction)
# for i in scene_emotion_prediction:
#   if not any(i.values()):
#     print(i)
#     print('yes')


if __name__ == '__main__':
    print(str(os.curdir))
    get_action_recognition('./test','test')