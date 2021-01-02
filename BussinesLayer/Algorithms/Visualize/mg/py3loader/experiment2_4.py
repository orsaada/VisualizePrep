import pickle
import moviegraphs
import videoindexer
from imdb import IMDb
from algo1 import algo_1
import json
import xlsxwriter


def cast_list(movie_id):
    """given the imdb id of a movie,
    returns a dictionary where the keys are associcated to the
    characters and the values are the actors that play them"""
    roles = dict()

    ia = IMDb()
    movie = ia.get_movie(movie_id[2:])

    for i in movie['cast']:
        actor = i["name"]
        character = i.currentRole
        if not isinstance(character, list):
            character = [character]
        for i in character:
            if "name" in i:
                roles[i["name"]] = actor

    return roles


def chars_in_scenes(scenes, chars):
    """return a list of actors given a list of tuples of start and end
    seconds of each scene, so characters[i] gives all the actors
    that appear between scenes[i][0] and scenes[i][1], according to VI"""
    res = []
    for (s, e) in scenes:
        characters = []
        for (c, apperances) in chars.items():
            for a in apperances:
                # if the two tuples (s,e) and (a[0], a[1]) overlap
                if (a[1] >= s and a[0] <= e):
                    characters.append(c)
        res.append(characters)
    return res


def char_precision(test_id, all_mg):
    """returns the precision of the face identification
    software comparing the VI results to the information
    on the MG dataset"""
    scenes = moviegraphs.load_scenes(test_id, all_mg)
    chars = videoindexer.get_character_app_dict(test_id)
    chars_vi = chars_in_scenes(scenes, chars)

    actors = cast_list(test_id)
    MG = all_mg[test_id]
    res = []
    data = []
    for i in MG.clip_graphs.values():
        res.append([actors[j] for j in i.get_nodes_of_type("entity") if j in actors])
    total, correct = 0, 0

    for i in range(len(chars_vi)):
        for j in range(len(chars_vi[i])):
            if 'Unknown' not in chars_vi[i][j]:
                if chars_vi[i][j] in res[i]:
                    correct += 1
                total += 1

    return round((correct / total * 100), 1) if total != 0 else 0

# return list of diffrence - start, end, list from vi, list from manual tagging
def get_diff(test_id, all_mg):
    scenes = moviegraphs.load_scenes(test_id, all_mg)
    chars = videoindexer.get_character_app_dict(test_id)
    chars_vi = chars_in_scenes(scenes, chars)

    actors = cast_list(test_id)
    MG = all_mg[test_id]
    res = []
    data = []
    for i in MG.clip_graphs.values():
        res.append([actors[j] for j in i.get_nodes_of_type("entity") if j in actors])
    total, correct = 0, 0

    for i in range(len(chars_vi)):
        data.append([(scenes[i][0]/60), (scenes[i][1]/60), chars_vi[i], res[i]])
        for j in range(len(chars_vi[i])):
            if 'Unknown' not in chars_vi[i][j]:
                if chars_vi[i][j] in res[i]:
                    correct += 1
                total += 1
    return data

def print_pretty():
    data = get_diff('tt0988595', all_mg)
    for obj in data:
        print(obj)
    return data
'''
workbook = xlsxwriter.Workbook('facial_identification_precision.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write(0, 0, 'IMDb id')
worksheet.write(0, 1, 'precision')

row = 1
with open('movie_list.txt', 'r') as f:
    for l in f:
        movie_id = l.split('\t')[0]
        precision = char_precision(movie_id, all_mg)
        worksheet.write(row, 0, movie_id)
        worksheet.write(row, 1, '{}%'.format(precision))
        row += 1

workbook.close()
'''


def open_all_mg():
    with open('2017-11-02-51-7637_py3.pkl', 'rb') as fid:
        all_mg = pickle.load(fid, encoding='latin1')
    return all_mg


with open('2017-11-02-51-7637_py3.pkl', 'rb') as fid:
    all_mg = pickle.load(fid, encoding='latin1')

print(char_precision('tt0988595', all_mg))
data_for_algo = print_pretty()
algo_1(data_for_algo)
with open('diff.json', 'w') as outfile:
    json.dump(data_for_algo, outfile)
