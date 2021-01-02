## Requirements
# python 3 (should work on most versions!)
# numpy
# networkx=1.11  NOTE: networkx-2 will NOT work because they changed many functions!

import pickle

with open('2017-11-02-51-7637_py3.pkl', 'rb') as fid:
    all_mg = pickle.load(fid, encoding='latin1')

# all_mg is a dictionary of MovieGraph objects
# indexed by imdb unique movie identifiers

scene_dir = '../../mg_videoinfo/scene_boundaries/'  # Change to your path
vid_dir = '../../mg_videoinfo/video_boundaries/'  # Change to your path


def load_scene_gt(all_mg, movie_id):
    scene_boundaries = []
    mg = all_mg[movie_id]

    for c in mg.clip_graphs:
        s = mg.clip_graphs[c].video['ss'] - 1
        e = mg.clip_graphs[c].video['es'] - 1
        scene_boundaries.append((s, e))

    return scene_boundaries


def load_vid_events(vid_dir, movie_id):
    vid_events = [(0, 0.0)]
    with open(vid_dir + movie_id + '.videvents', 'r') as f:
        for row in f:
            if len(row.split(' ')) != 3:
                continue
            row = row[:-1]
            frame = int(row.split(' ')[0])
            timestamp = float(row.split(' ')[1])
            vid_events.append((frame, timestamp))

    with open(vid_dir + movie_id + '.matidx', 'r') as frame_file:
        lines = frame_file.read().splitlines()
        last_line = lines[-1]
        if last_line != '\n':
            vid_events.append((int(last_line.split(' ')[0]), float(last_line.split(' ')[1])))
        else:
            print("Wrong last line!")

    return vid_events


def compute_scene_boundaries(scenes, videvents, fps=24, offset=0):
    scenes_from_to = []

    for (_ss, _es) in scenes:
        _from = videvents[_ss][1] + offset
        _to = videvents[_es + 1][1] - 1 / fps + offset
        scenes_from_to.append((_from, _to))

    return scenes_from_to


def load_scenes(test_id, all_mg):
    scene_boundaries = load_scene_gt(all_mg, test_id)
    vid_events = load_vid_events(vid_dir, test_id)
    test_movie_scenes = compute_scene_boundaries(scene_boundaries, vid_events)
    # Eventually, test_movie_scenes is a list of tuples
    # Each tuple is the start/end timestamp of each scene
    return test_movie_scenes


def load_cuts(vid_dir, movie_id):
    with open(vid_dir + movie_id + '.videvents', 'r') as f:
        f.readline()
        return [float(row.split(' ')[1]) for row in f if f]







