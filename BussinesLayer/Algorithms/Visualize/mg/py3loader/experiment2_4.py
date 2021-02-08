import pickle
import moviegraphs
import videoindexer
from imdb import IMDb
from BussinesLayer.Algorithms.Visualize.mg.py3loader.algorithm import union_algorithm,pipeline_algorithm,algorithm_1,algorithm_2_improved,algorithm_faces_speakers,create_faces_list
import datetime
import time
from BussinesLayer.Algorithms.Visualize.mg.py3loader.videoindexer import time_to_secs

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


def chars_in_scenes_with_duplicate(scenes, chars):
    """return a list of actors given a list of tuples of start and end
    seconds of each scene, so characters[i] gives all the actors
    that appear between scenes[i][0] and scenes[i][1], according to VI"""
    res = []
    for (s, e) in scenes:
        characters = []
        for (c, apperances) in chars.items():
            for a in apperances:
                # if the two tuples (s,e) and (a[0], a[1]) overlap
                if time_to_secs(a[1]) >= s and time_to_secs(a[0]) <= e:
                    characters.append(c)
        res.append(characters)
    return res


def chars_in_scenes_with_duplicate2(scenes, beforeData):  # maybe need to fix
    res = []
    for (s, e) in scenes:
        characters = []
        for (start, end, name) in beforeData:
            # if the two tuples (s,e) and (a[0], a[1]) overlap
            #x = time.strptime(start.split('.')[0], '%H:%M:%S')
            #newS = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
            #x = time.strptime(end.split('.')[0], '%H:%M:%S')
            #newE = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
            newS = time_to_secs(start)
            newE = time_to_secs(end)
            if newE >= s and newS <= e:
                characters.append(name)
        res.append(characters)
    return res


def char_precision(test_id, all_mg, num, data, kind):
    """returns the precision of the face identification
    software comparing the VI results to the information
    on the MG dataset"""
    scenes = moviegraphs.load_scenes(test_id, all_mg)
    if kind == 'with':
        if num == 1:
            chars = videoindexer.get_character_app_dict(test_id)
            chars_vi = chars_in_scenes_with_duplicate(scenes, chars)
        elif num == 2:
            chars_vi = chars_in_scenes_with_duplicate2(scenes, data)
    else:
        if num == 1:
            chars = videoindexer.get_character_app_dict(test_id)
            chars_vi = chars_in_scenes_without_duplicate(scenes, chars)
        elif num == 2:
            chars_vi = chars_in_scenes_without_duplicate2(scenes, data)
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
                    correct += 1  # true positive
                total += 1  # false positive + true positive
    return round((correct / total * 100), 1) if total != 0 else 0


def char_recall(test_id, all_mg, num, data, kind):
    """returns the recall of the face identification
    software comparing the VI results to the information
    on the MG dataset"""
    scenes = moviegraphs.load_scenes(test_id, all_mg)
    if kind == 'with':
        if num == 1:
            chars = videoindexer.get_character_app_dict(test_id)
            chars_vi = chars_in_scenes_with_duplicate(scenes, chars)
        elif num == 2:
            chars_vi = chars_in_scenes_with_duplicate2(scenes, data)
    else:
        if num == 1:
            chars = videoindexer.get_character_app_dict(test_id)
            chars_vi = chars_in_scenes_without_duplicate(scenes, chars)
        elif num == 2:
            chars_vi = chars_in_scenes_without_duplicate2(scenes, data)
    actors = cast_list(test_id)
    MG = all_mg[test_id]
    res = []
    for i in MG.clip_graphs.values():
        res.append([actors[j] for j in i.get_nodes_of_type("entity") if j in actors])
    fn, tp = 0, 0

    for i in range(len(chars_vi)):
        for j in range(len(chars_vi[i])):
            if 'Unknown' not in chars_vi[i][j]:
                if chars_vi[i][j] in res[i]:
                    tp += 1  # true positive
    for i in range(len(res)):
        if res[i] not in chars_vi[i]:
            fn += 1  # false negative
    total = fn + tp
    return round((tp / total * 100), 1) if total != 0 else 0


def get_percentage(group1, group2):
    hits = 0
    new_group1 = list(dict.fromkeys(group1))
    for element in new_group1:
        if 'Unknown' not in element:
            if element in group2:
                hits += 1
    if len(group2) == 0:
        return 0
    else:
        return (hits/len(group2))*100


def get_diff(test_id, all_mg, num, data, kind):
    scenes = moviegraphs.load_scenes(test_id, all_mg)
    if kind == 'with':
        if num == 1:
            chars = videoindexer.get_character_app_dict(test_id)
            chars_vi = chars_in_scenes_with_duplicate(scenes, chars)
        elif num == 2:
            chars_vi = chars_in_scenes_with_duplicate2(scenes, data)
    else:
        if num == 1:
            chars = videoindexer.get_character_app_dict(test_id)
            chars_vi = chars_in_scenes_without_duplicate(scenes, chars)
        elif num == 2:
            chars_vi = chars_in_scenes_without_duplicate2(scenes, data)
    actors = cast_list(test_id)
    MG = all_mg[test_id]
    res = []
    data = []
    for i in MG.clip_graphs.values():
        res.append([actors[j] for j in i.get_nodes_of_type("entity") if j in actors])

    for i in range(len(chars_vi)):
        percentage = get_percentage(chars_vi[i], res[i])
        data.append([(scenes[i][0]/60), (scenes[i][1]/60), list(dict.fromkeys(chars_vi[i])), res[i], percentage])
    return data


def chars_in_scenes_without_duplicate(scenes, chars):
    """return a list of actors given a list of tuples of start and end
    seconds of each scene, so characters[i] gives all the actors
    that appear between scenes[i][0] and scenes[i][1], according to VI"""
    res = []
    for (s, e) in scenes:
        characters = []
        for (c, apperances) in chars.items():
            for a in apperances:
                # if the two tuples (s,e) and (a[0], a[1]) overlap
                if time_to_secs(a[1]) >= s and time_to_secs(a[0]) <= e:
                    characters.append(c)
        characters_removed_duplicated_items = list(dict.fromkeys(characters))
        res.append(characters_removed_duplicated_items)
    return res


def chars_in_scenes_without_duplicate2(scenes, beforeData):  # maybe need to fix
    res = []
    for (s, e) in scenes:
        characters = []
        for (start, end, name) in beforeData:
            # if the two tuples (s,e) and (a[0], a[1]) overlap
            newS = time_to_secs(start)
            newE = time_to_secs(end)
            if newE >= s and newS <= e:
                characters.append(name)
        characters_removed_duplicated_items = list(dict.fromkeys(characters))
        res.append(characters_removed_duplicated_items)
    return res


def print_pretty_differences_test(tt_movie, kind):
    print("[ start , end ,[Movie Indexer Actors] , [Manual Info Actors] , percentage ]:")
    data_b = get_diff(tt_movie, all_mg, 1, "", kind)
    for obj in data_b:
        print(obj)


def print_pretty_differences(json_movie_id, kind):
    faces_list = create_faces_list("./../../vi_json/"+json_movie_id+".json")
    res1 = algorithm_2_improved("./../../vi_json/"+json_movie_id+".json", faces_list)
    print("[ start , end ,[Movie Indexer Actors] , [Manual Info Actors] , percentage ]:")
    print("Before algo:")
    data_b = get_diff(json_movie_id, all_mg, 1, "", kind)
    for obj in data_b:
        print(obj)
    print("After algo:")
    data_a = get_diff(json_movie_id, all_mg, 2, res1, kind)
    for obj in data_a:
        print(obj)


with open('2017-11-02-51-7637_py3.pkl', 'rb') as fid:
    all_mg = pickle.load(fid, encoding='latin1')


def print_pretty_changes_algorithm(kind, algorithm):
    dress_27 = "./../../vi_json/tt0988595.json"
    crazy_stupid_love = "./../../vi_json/tt1570728.json"
    flight = "./../../vi_json/tt1907668.json"
    forrest_gump = "./../../vi_json/tt0109830.json"
    up_in_the_air = "./../../vi_json/tt1193138.json"

    if algorithm == 1:
        res4 = algorithm_1(dress_27, create_faces_list(dress_27))
        res1 = algorithm_1(crazy_stupid_love, create_faces_list(crazy_stupid_love))
        res2 = algorithm_1(flight, create_faces_list(flight))
        res3 = algorithm_1(forrest_gump, create_faces_list(forrest_gump))
        res5 = algorithm_1(up_in_the_air, create_faces_list(up_in_the_air))
    if algorithm == 2:
        res1 = algorithm_2_improved(crazy_stupid_love,create_faces_list(crazy_stupid_love))
        res2 = algorithm_2_improved(flight,create_faces_list(flight))
        res3 = algorithm_2_improved(forrest_gump,create_faces_list(forrest_gump))
        res4 = algorithm_2_improved(dress_27,create_faces_list(dress_27))
        res5 = algorithm_2_improved(up_in_the_air,create_faces_list(up_in_the_air))
    if algorithm == 3:
        res1 = algorithm_faces_speakers( crazy_stupid_love,create_faces_list(crazy_stupid_love))
        res2 = algorithm_faces_speakers(flight,create_faces_list(flight))
        res3 = algorithm_faces_speakers( forrest_gump,create_faces_list(forrest_gump))
        res4 = algorithm_faces_speakers(dress_27,create_faces_list(dress_27))
        res5 = algorithm_faces_speakers(up_in_the_air,create_faces_list(up_in_the_air))
    if algorithm == 4:
        res1 = pipeline_algorithm([algorithm_faces_speakers,algorithm_2_improved],
            crazy_stupid_love
            )
        res2 = pipeline_algorithm([algorithm_faces_speakers,algorithm_2_improved],
            flight)
        res3 = pipeline_algorithm([algorithm_faces_speakers,algorithm_2_improved],
            forrest_gump)
        res4 = pipeline_algorithm([algorithm_faces_speakers,algorithm_2_improved],
            dress_27)
        res5 = pipeline_algorithm([algorithm_faces_speakers,algorithm_2_improved],
            up_in_the_air)
    if algorithm == 5:
        res1 = pipeline_algorithm([algorithm_2_improved,algorithm_faces_speakers],
            crazy_stupid_love
            )
        res2 = pipeline_algorithm([algorithm_2_improved,algorithm_faces_speakers],
            flight)
        res3 = pipeline_algorithm([algorithm_2_improved,algorithm_faces_speakers],
            forrest_gump)
        res4 = pipeline_algorithm([algorithm_2_improved,algorithm_faces_speakers],
            dress_27)
        res5 = pipeline_algorithm([algorithm_2_improved,algorithm_faces_speakers],
            up_in_the_air)
    if algorithm == 6:
        res1 = union_algorithm(algorithm_2_improved,algorithm_faces_speakers,
            crazy_stupid_love
            )
        res2 =union_algorithm(algorithm_2_improved,algorithm_faces_speakers,
            flight)
        res3 = union_algorithm(algorithm_2_improved,algorithm_faces_speakers,
            forrest_gump)
        res4 = union_algorithm(algorithm_2_improved,algorithm_faces_speakers,
            dress_27)
        res5 = union_algorithm(algorithm_2_improved,algorithm_faces_speakers,
            up_in_the_air)

    print("27 dress:\nprecision before - " + str(char_precision('tt0988595', all_mg, 1, "", kind)))
    print('precision after - ' + str(char_precision('tt0988595', all_mg, 2, res4, kind)))
    print('recall before - ' + str(char_recall('tt0988595', all_mg, 1, "", kind)))
    print('recall after - ' + str(char_recall('tt0988595', all_mg, 2, res4, kind)) + '\n')

    print("crazy stupid love:\nprecision before - " + str(char_precision('tt1570728', all_mg, 1, "", kind)))
    print('precision after - ' + str(char_precision('tt1570728', all_mg, 2, res1, kind)))
    print('recall before - ' + str(char_recall('tt1570728', all_mg, 1, "", kind)))
    print('recall after - ' + str(char_recall('tt1570728', all_mg, 2, res1, kind)) + '\n')

    print("flight:\nprecision before - " + str(char_precision('tt1907668', all_mg, 1, "", kind)))
    print('precision after - ' + str(char_precision('tt1907668', all_mg, 2, res2, kind)))
    print('recall before - ' + str(char_recall('tt1907668', all_mg, 1, "", kind)))
    print('recall after - ' + str(char_recall('tt1907668', all_mg, 2, res2, kind)) + '\n')

    print("forest gump:\nprecision before - " + str(char_precision('tt0109830', all_mg, 1, "", kind)))
    print('precision after - ' + str(char_precision('tt0109830', all_mg, 2, res3, kind)))
    print('recall before - ' + str(char_recall('tt0109830', all_mg, 1, "", kind)))
    print('recall after - ' + str(char_recall('tt0109830', all_mg, 2, res3, kind)) + '\n')

    print("up in the air:\nprecision before - " + str(char_precision('tt1193138', all_mg, 1, "", kind)))
    print('precision after - ' + str(char_precision('tt1193138', all_mg, 2, res5, kind)))
    print('recall before - ' + str(char_recall('tt1193138', all_mg, 1, "", kind)))
    print('recall after - ' + str(char_recall('tt1193138', all_mg, 2, res5, kind)) + '\n')


print_pretty_changes_algorithm('with', 1)
print_pretty_changes_algorithm('without', 1)

print_pretty_changes_algorithm('with', 2)
print_pretty_changes_algorithm('without', 2)

print_pretty_changes_algorithm('with', 3)
print_pretty_changes_algorithm('without', 3)
'''
print_pretty_changes_algorithm('with', 4)
print_pretty_changes_algorithm('without', 4)

print_pretty_changes_algorithm('with', 5)
print_pretty_changes_algorithm('without', 5)

print_pretty_changes_algorithm('with', 6)
print_pretty_changes_algorithm('without', 6)

print_pretty_differences('tt0988595', 'with')
print_pretty_differences_test('tt0988595')
'''
