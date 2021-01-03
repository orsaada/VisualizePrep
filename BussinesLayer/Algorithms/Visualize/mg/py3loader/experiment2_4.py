import pickle
import moviegraphs
import videoindexer
from imdb import IMDb
import json
import xlsxwriter
from BussinesLayer.Algorithms.Visualize.mg.py3loader.algorithm import algorithm_1
import datetime
import time


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


def chars_in_scenes2(scenes, beforeData):
    res = []
    for (s, e) in scenes:
        characters = []
        for (start, end, name) in beforeData:
            # if the two tuples (s,e) and (a[0], a[1]) overlap
            x = time.strptime(start.split('.')[0], '%H:%M:%S')
            newS = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
            x = time.strptime(end.split('.')[0], '%H:%M:%S')
            newE = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
            if newE >= s and newS <= e:
                characters.append(name)
        res.append(characters)
    return res


def char_precision(test_id, all_mg, num, data):
    """returns the precision of the face identification
    software comparing the VI results to the information
    on the MG dataset"""
    scenes = moviegraphs.load_scenes(test_id, all_mg)
    if num == 1:
        chars = videoindexer.get_character_app_dict(test_id)
        chars_vi = chars_in_scenes(scenes, chars)
    elif num == 2:
        chars_vi = chars_in_scenes2(scenes, data)
    actors = cast_list(test_id)
    MG = all_mg[test_id]
    res = []
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


def print_pretty_differences(tt_movie):
    data = get_diff(tt_movie, all_mg)
    print("[ start , end ,[Movie Indexer Actors] , [Manual Info Actors] ]:")
    for obj in data:
        print(obj)


with open('2017-11-02-51-7637_py3.pkl', 'rb') as fid:
    all_mg = pickle.load(fid, encoding='latin1')


def print_pretty_changes_algorithm_1():
    res1 = algorithm_1("../../vi_json/tt1570728.json")
    res2 = algorithm_1("../../vi_json/tt1907668.json")
    res3 = algorithm_1("../../vi_json/tt0109830.json")
    res4 = algorithm_1("../../vi_json/tt0988595.json")

    print("crazy stupid love:\nbefore - " + str(char_precision('tt1570728', all_mg, 1, "")))
    print('after - ' + str(char_precision('tt1570728', all_mg, 2, res1)) + '\n')

    print("flight:\nbefore - " + str(char_precision('tt1907668', all_mg, 1, "")))
    print('after - ' + str(char_precision('tt1907668', all_mg, 2, res2)) + '\n')

    print("forest gump:\nbefore - " + str(char_precision('tt0109830', all_mg, 1, "")))
    print('after - ' + str(char_precision('tt0109830', all_mg, 2, res3)) + '\n')

    print("27 dress:\nbefore - " + str(char_precision('tt0988595', all_mg, 1, "")))
    print('after - ' + str(char_precision('tt0988595', all_mg, 2, res4)) + '\n')


print_pretty_changes_algorithm_1()
print_pretty_differences('tt0988595')
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


# Or Added
def open_all_mg():
    with open('2017-11-02-51-7637_py3.pkl', 'rb') as fid:
        all_mg = pickle.load(fid, encoding='latin1')
    return all_mg


with open('2017-11-02-51-7637_py3.pkl', 'rb') as fid:
    all_mg = pickle.load(fid, encoding='latin1')

# print(char_precision('tt0988595', all_mg))
# data_for_algo = print_pretty()
# algo_1(data_for_algo)
# with open('diff.json', 'w') as outfile:
#     json.dump(data_for_algo, outfile)
