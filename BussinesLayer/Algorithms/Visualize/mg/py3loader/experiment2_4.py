import json
import pickle
from pathlib import Path
from BussinesLayer.Algorithms.Visualize.mg.py3loader import moviegraphs
from BussinesLayer.Algorithms.Visualize.mg.py3loader import videoindexer
from imdb import IMDb
from BussinesLayer.Algorithms.Visualize.mg.py3loader.algorithm import pipeline_algorithm, algorithm_1,\
    algorithm_2_improved, algorithm_faces_speakers, create_faces_list
from BussinesLayer.Algorithms.Visualize.mg.py3loader.videoindexer import time_to_secs

dress_27 = "./../../vi_json/tt0988595.json"
crazy_stupid_love = "./../../vi_json/tt1570728.json"
flight = "./../../vi_json/tt1907668.json"
forrest_gump = "./../../vi_json/tt0109830.json"
up_in_the_air = "./../../vi_json/tt1193138.json"
the_help = "./../../vi_json/tt1454029.json"
the_godfather = "./../../vi_json/tt0068646.json"
the_ugly_truth = "./../../vi_json/tt1142988.json"
the_lost_weekend = "./../../vi_json/tt0037884.json"
knocked_up = "./../../vi_json/tt0478311.json"
as_good_as_it_gets = "./../../vi_json/tt0119822.json"
four_weddings_and_a_funeral = "./../../vi_json/tt0109831.json"
one_flew_over_the_cuckoos_nest = "./../../vi_json/tt0073486.json"
juno = "./../../vi_json/tt0467406.json"
lincoln_lawyer = "./../../vi_json/tt1189340.json"
match_point = "./../../vi_json/tt0416320.json"
ocean_eleven = "./../../vi_json/tt0240772.json"
pulp_fiction = "./../../vi_json/tt0110912.json"
the_day_the_earth_stood_still = "./../../vi_json/tt0970416.json"
the_social_network = "./../../vi_json/tt1285016.json"


def cast_list(movie_id):
    """given the imdb id of a movie,
    returns a dictionary where the keys are associcated to the
    characters and the values are the actors that play them"""
    roles = dict()
    # print(movie_id[2:])
    base_path = Path(__file__).parent.parent.parent
    # print(base_path / 'vi_json/{}.json'.format(movie_id))

    try:
        ia = IMDb(accessSystem='http', reraiseExceptions=True)
        movie = ia.get_movie(movie_id[2:])
    except:
        print("error")
    # print(movie['cast'])
    # try:
    #     ia = IMDb(accessSystem='http', reraiseExceptions=True)
    #     movie = ia.get_movie(movie_id[2:])
    # except:
    #     print("error")

    # print(movie['cast'])
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


def jaccard_per_scene(vi_actors_in_scene, mg_actors_in_scene):
    vi_actors_group = set(vi_actors_in_scene)
    mg_actors_group = set(mg_actors_in_scene)
    intersection = vi_actors_group.intersection(mg_actors_group)
    union = vi_actors_group.union(mg_actors_group)
    if len(union) == 0:
        return 0
    return len(intersection) / len(union)


def jaccard_avarage(jaccard_per_scene_list):
    return sum(jaccard_per_scene_list) / len(jaccard_per_scene_list)


def jaccard(test_id, all_mg, num, data, kind):
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
    jaccard_list = []

    for i in range(len(chars_vi)):
        jaccard_list.append(jaccard_per_scene(chars_vi[i], res[i]))

    return jaccard_avarage(jaccard_list)


def f_score(precision, recall):
    if float(precision) + float(recall) != 0:
        return 2 * (float(precision) * float(recall)) / (float(precision) + float(recall))
    return 0


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
    all_mg = get_mg()
    print("[ start , end ,[Movie Indexer Actors] , [Manual Info Actors] , percentage ]:")
    data_b = get_diff(tt_movie, all_mg, 1, "", kind)
    for obj in data_b:
        print(obj)


def print_pretty_differences(json_movie_id, kind):
    all_mg = get_mg()
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


def get_mg():
    base_path = Path(__file__).parent
    # file_path = (base_path / 'config.json').resolve()

    with open(base_path / '2017-11-02-51-7637_py3.pkl', 'rb') as fid:
        all_mg = pickle.load(fid, encoding='latin1')
    return all_mg


def print_pretty_changes_algorithm(kind, algorithm):
    all_mg = get_mg()

    movies = []
    if algorithm == 1:
        movies = [
            ("dress 27", dress_27, 'tt0988595', algorithm_1(dress_27, create_faces_list(dress_27))),
            ("crazy stupid love", crazy_stupid_love, 'tt1570728', algorithm_1(crazy_stupid_love, create_faces_list(crazy_stupid_love))),
            ("flight", flight, 'tt1907668', algorithm_1(flight, create_faces_list(flight))),
            ("forrest gump", forrest_gump, 'tt0109830', algorithm_1(forrest_gump, create_faces_list(forrest_gump))),
            ("up in the air", up_in_the_air, 'tt1193138', algorithm_1(up_in_the_air, create_faces_list(up_in_the_air))),
            ("the help", the_help, 'tt1454029', algorithm_1(the_help, create_faces_list(the_help))),
            ("the godfather", the_godfather, 'tt0068646', algorithm_1(the_godfather, create_faces_list(the_godfather))),
            ("the ugly truth", the_ugly_truth, 'tt1142988', algorithm_1(the_ugly_truth, create_faces_list(the_ugly_truth))),
            ("the_lost_weekend", the_lost_weekend, 'tt0037884', algorithm_1(the_lost_weekend, create_faces_list(the_lost_weekend))),
            ("knocked up", knocked_up, 'tt0478311', algorithm_1(knocked_up, create_faces_list(knocked_up))),
            ("as_good_as_it_gets", as_good_as_it_gets, 'tt0119822', algorithm_1(as_good_as_it_gets, create_faces_list(as_good_as_it_gets))),
            ("four weddings and a funeral", four_weddings_and_a_funeral, 'tt0109831', algorithm_1(four_weddings_and_a_funeral, create_faces_list(four_weddings_and_a_funeral))),
            ("one flew over the cuckoos nest", one_flew_over_the_cuckoos_nest, 'tt0073486', algorithm_1(one_flew_over_the_cuckoos_nest, create_faces_list(one_flew_over_the_cuckoos_nest))),
            ("juno", juno, 'tt0467406', algorithm_1(juno, create_faces_list(juno))),
            ("lincoln lawyer", lincoln_lawyer, 'tt1189340', algorithm_1(lincoln_lawyer, create_faces_list(lincoln_lawyer))),
            ("match point", match_point, 'tt0416320', algorithm_1(match_point, create_faces_list(match_point))),
            ("ocean eleven", ocean_eleven, 'tt0240772', algorithm_1(ocean_eleven, create_faces_list(ocean_eleven))),
            ("pulp fiction", pulp_fiction, 'tt0110912', algorithm_1(pulp_fiction, create_faces_list(pulp_fiction))),
            ("the day the earth stood still", the_day_the_earth_stood_still, 'tt0970416', algorithm_1(the_day_the_earth_stood_still, create_faces_list(the_day_the_earth_stood_still))),
            ("the social network", the_social_network, 'tt1285016', algorithm_1(the_social_network, create_faces_list(the_social_network)))
        ]
    if algorithm == 2:
        movies = [
            ("dress 27", dress_27, 'tt0988595', algorithm_2_improved(dress_27, create_faces_list(dress_27))),
            ("crazy stupid love", crazy_stupid_love, 'tt1570728',
             algorithm_2_improved(crazy_stupid_love, create_faces_list(crazy_stupid_love))),
            ("flight", flight, 'tt1907668', algorithm_2_improved(flight, create_faces_list(flight))),
            ("forrest gump", forrest_gump, 'tt0109830', algorithm_2_improved(forrest_gump, create_faces_list(forrest_gump))),
            ("up in the air", up_in_the_air, 'tt1193138', algorithm_2_improved(up_in_the_air, create_faces_list(up_in_the_air))),
            ("the help", the_help, 'tt1454029', algorithm_2_improved(the_help, create_faces_list(the_help))),
            ("the godfather", the_godfather, 'tt0068646', algorithm_2_improved(the_godfather, create_faces_list(the_godfather))),
            ("the ugly truth", the_ugly_truth, 'tt1142988',
             algorithm_2_improved(the_ugly_truth, create_faces_list(the_ugly_truth))),
            ("the_lost_weekend", the_lost_weekend, 'tt0037884',
             algorithm_2_improved(the_lost_weekend, create_faces_list(the_lost_weekend))),
            ("knocked up", knocked_up, 'tt0478311', algorithm_2_improved(knocked_up, create_faces_list(knocked_up))),
            ("as_good_as_it_gets", as_good_as_it_gets, 'tt0119822',
             algorithm_2_improved(as_good_as_it_gets, create_faces_list(as_good_as_it_gets))),
            ("four weddings and a funeral", four_weddings_and_a_funeral, 'tt0109831',
             algorithm_2_improved(four_weddings_and_a_funeral, create_faces_list(four_weddings_and_a_funeral))),
            ("one flew over the cuckoos nest", one_flew_over_the_cuckoos_nest, 'tt0073486',
             algorithm_2_improved(one_flew_over_the_cuckoos_nest, create_faces_list(one_flew_over_the_cuckoos_nest))),
            ("juno", juno, 'tt0467406', algorithm_2_improved(juno, create_faces_list(juno))),
            ("lincoln lawyer", lincoln_lawyer, 'tt1189340',
             algorithm_2_improved(lincoln_lawyer, create_faces_list(lincoln_lawyer))),
            ("match point", match_point, 'tt0416320', algorithm_2_improved(match_point, create_faces_list(match_point))),
            ("ocean eleven", ocean_eleven, 'tt0240772', algorithm_2_improved(ocean_eleven, create_faces_list(ocean_eleven))),
            ("pulp fiction", pulp_fiction, 'tt0110912', algorithm_2_improved(pulp_fiction, create_faces_list(pulp_fiction))),
            ("the day the earth stood still", the_day_the_earth_stood_still, 'tt0970416',
             algorithm_2_improved(the_day_the_earth_stood_still, create_faces_list(the_day_the_earth_stood_still))),
            ("the social network", the_social_network, 'tt1285016',
             algorithm_2_improved(the_social_network, create_faces_list(the_social_network)))
        ]
    if algorithm == 3:
        movies = [
            ("dress 27", dress_27, 'tt0988595', algorithm_faces_speakers(dress_27, create_faces_list(dress_27))),
            ("crazy stupid love", crazy_stupid_love, 'tt1570728',
             algorithm_faces_speakers(crazy_stupid_love, create_faces_list(crazy_stupid_love))),
            ("flight", flight, 'tt1907668', algorithm_faces_speakers(flight, create_faces_list(flight))),
            ("forrest gump", forrest_gump, 'tt0109830', algorithm_faces_speakers(forrest_gump, create_faces_list(forrest_gump))),
            ("up in the air", up_in_the_air, 'tt1193138', algorithm_faces_speakers(up_in_the_air, create_faces_list(up_in_the_air))),
            ("the help", the_help, 'tt1454029', algorithm_faces_speakers(the_help, create_faces_list(the_help))),
            ("the godfather", the_godfather, 'tt0068646', algorithm_faces_speakers(the_godfather, create_faces_list(the_godfather))),
            ("the ugly truth", the_ugly_truth, 'tt1142988',
             algorithm_faces_speakers(the_ugly_truth, create_faces_list(the_ugly_truth))),
            ("the_lost_weekend", the_lost_weekend, 'tt0037884',
             algorithm_faces_speakers(the_lost_weekend, create_faces_list(the_lost_weekend))),
            ("knocked up", knocked_up, 'tt0478311', algorithm_faces_speakers(knocked_up, create_faces_list(knocked_up))),
            ("as_good_as_it_gets", as_good_as_it_gets, 'tt0119822',
             algorithm_faces_speakers(as_good_as_it_gets, create_faces_list(as_good_as_it_gets))),
            ("four weddings and a funeral", four_weddings_and_a_funeral, 'tt0109831',
             algorithm_faces_speakers(four_weddings_and_a_funeral, create_faces_list(four_weddings_and_a_funeral))),
            ("one flew over the cuckoos nest", one_flew_over_the_cuckoos_nest, 'tt0073486',
             algorithm_faces_speakers(one_flew_over_the_cuckoos_nest, create_faces_list(one_flew_over_the_cuckoos_nest))),
            ("juno", juno, 'tt0467406', algorithm_faces_speakers(juno, create_faces_list(juno))),
            ("lincoln lawyer", lincoln_lawyer, 'tt1189340',
             algorithm_faces_speakers(lincoln_lawyer, create_faces_list(lincoln_lawyer))),
            ("match point", match_point, 'tt0416320', algorithm_faces_speakers(match_point, create_faces_list(match_point))),
            ("ocean eleven", ocean_eleven, 'tt0240772', algorithm_faces_speakers(ocean_eleven, create_faces_list(ocean_eleven))),
            ("pulp fiction", pulp_fiction, 'tt0110912', algorithm_faces_speakers(pulp_fiction, create_faces_list(pulp_fiction))),
            ("the day the earth stood still", the_day_the_earth_stood_still, 'tt0970416',
             algorithm_faces_speakers(the_day_the_earth_stood_still, create_faces_list(the_day_the_earth_stood_still))),
            ("the social network", the_social_network, 'tt1285016',
             algorithm_faces_speakers(the_social_network, create_faces_list(the_social_network)))
        ]
    if algorithm == 4:
        movies = [
            ("dress 27", dress_27, 'tt0988595', pipeline_algorithm([algorithm_faces_speakers, algorithm_2_improved, algorithm_1], dress_27)),
            ("crazy stupid love", crazy_stupid_love, 'tt1570728',
             pipeline_algorithm([algorithm_faces_speakers, algorithm_2_improved, algorithm_1], crazy_stupid_love)),
            ("flight", flight, 'tt1907668', pipeline_algorithm([algorithm_faces_speakers,algorithm_2_improved, algorithm_1], flight)),
            ("forrest gump", forrest_gump, 'tt0109830', pipeline_algorithm([algorithm_faces_speakers, algorithm_2_improved, algorithm_1], forrest_gump)),
            ("up in the air", up_in_the_air, 'tt1193138', pipeline_algorithm([algorithm_faces_speakers, algorithm_2_improved, algorithm_1], up_in_the_air)),
            ("the help", the_help, 'tt1454029', pipeline_algorithm([algorithm_faces_speakers,algorithm_2_improved, algorithm_1], the_help)),
            ("the godfather", the_godfather, 'tt0068646', pipeline_algorithm([algorithm_faces_speakers, algorithm_2_improved, algorithm_1], the_godfather)),
            ("the ugly truth", the_ugly_truth, 'tt1142988',
             pipeline_algorithm([algorithm_faces_speakers, algorithm_2_improved, algorithm_1], the_ugly_truth)),
            ("the_lost_weekend", the_lost_weekend, 'tt0037884',
             pipeline_algorithm([algorithm_faces_speakers, algorithm_2_improved, algorithm_1], the_lost_weekend)),
            ("knocked up", knocked_up, 'tt0478311', pipeline_algorithm([algorithm_faces_speakers, algorithm_2_improved, algorithm_1], knocked_up)),
            ("as_good_as_it_gets", as_good_as_it_gets, 'tt0119822',
             pipeline_algorithm([algorithm_faces_speakers, algorithm_2_improved, algorithm_1], as_good_as_it_gets)),
            ("four weddings and a funeral", four_weddings_and_a_funeral, 'tt0109831',
             pipeline_algorithm([algorithm_faces_speakers, algorithm_2_improved, algorithm_1], four_weddings_and_a_funeral)),
            ("one flew over the cuckoos nest", one_flew_over_the_cuckoos_nest, 'tt0073486',
             pipeline_algorithm([algorithm_faces_speakers, algorithm_2_improved, algorithm_1], one_flew_over_the_cuckoos_nest)),
            ("juno", juno, 'tt0467406', pipeline_algorithm([algorithm_faces_speakers, algorithm_2_improved, algorithm_1], juno)),
            ("lincoln lawyer", lincoln_lawyer, 'tt1189340',
             pipeline_algorithm([algorithm_faces_speakers, algorithm_2_improved, algorithm_1], lincoln_lawyer)),
            ("match point", match_point, 'tt0416320', pipeline_algorithm([algorithm_faces_speakers, algorithm_2_improved, algorithm_1], match_point)),
            ("ocean eleven", ocean_eleven, 'tt0240772', pipeline_algorithm([algorithm_faces_speakers, algorithm_2_improved, algorithm_1], ocean_eleven)),
            ("pulp fiction", pulp_fiction, 'tt0110912', pipeline_algorithm([algorithm_faces_speakers, algorithm_2_improved, algorithm_1], pulp_fiction)),
            ("the day the earth stood still", the_day_the_earth_stood_still, 'tt0970416',
             pipeline_algorithm([algorithm_faces_speakers, algorithm_2_improved, algorithm_1], the_day_the_earth_stood_still)),
            ("the social network", the_social_network, 'tt1285016',
             pipeline_algorithm([algorithm_faces_speakers, algorithm_2_improved, algorithm_1], the_social_network))
        ]
    for (name, path, tt, alg) in movies:
        before_precision = str(char_precision(tt, all_mg, 1, "", kind))
        after_precision = str(char_precision(tt, all_mg, 2, alg, kind))
        before_recall = str(char_recall(tt, all_mg, 1, "", kind))
        after_recall = str(char_recall(tt, all_mg, 2, alg, kind))
        before_jaccard = str(jaccard(tt, all_mg, 1, "", kind))
        after_jaccard = str(jaccard(tt, all_mg, 2, alg, kind))
        print(name+":\nprecision before - " + before_precision)
        print('precision after - ' + after_precision)
        print('recall before - ' + before_recall)
        print('recall after - ' + after_recall)
        print('jaccard before - ' + before_jaccard)
        print('jaccard after - ' + after_jaccard)
        print('f score before - ' + str(f_score(before_precision, before_recall)))
        print('f score after - ' + str(f_score(after_precision, after_recall)) + '\n')


def get_insight(tt, movie_path, algorithm):
    all_mg = get_mg()
    base_path = Path(__file__).parent.parent.parent
    movie_path = base_path / "vi_json/{}.json".format(movie_path)
    alg = ""
    if algorithm == 1:
        alg = algorithm_1(movie_path, create_faces_list(movie_path))
    elif algorithm == 2:
        alg = algorithm_2_improved(movie_path, create_faces_list(movie_path))
    elif algorithm == 3:
        alg = algorithm_faces_speakers(movie_path, create_faces_list(movie_path))
    elif algorithm == 4:
        alg = pipeline_algorithm([algorithm_faces_speakers, algorithm_2_improved, algorithm_1], movie_path)
    before_precision = str(char_precision(tt, all_mg, 1, "", 'with'))
    after_precision = str(char_precision(tt, all_mg, 2, alg, 'with'))
    before_recall = str(char_recall(tt, all_mg, 1, "", 'with'))
    after_recall = str(char_recall(tt, all_mg, 2, alg, 'with'))
    before_jaccard = str(jaccard(tt, all_mg, 1, "", 'with'))
    after_jaccard = str(jaccard(tt, all_mg, 2, alg, 'with'))
    before_f_score = f_score(before_precision, before_recall)
    after_f_score = f_score(after_precision, after_recall)
    return [before_precision, before_recall, before_jaccard, before_f_score], [after_precision, after_recall, after_jaccard, after_f_score]


def get_data(tt, alg):
    all_mg = get_mg()
    movie_json = {}
    before_precision = str(char_precision(tt, all_mg, 1, "", 'with'))
    after_precision = str(char_precision(tt, all_mg, 2, alg, 'with'))
    before_recall = str(char_recall(tt, all_mg, 1, "", 'with'))
    after_recall = str(char_recall(tt, all_mg, 2, alg, 'with'))
    before_jaccard = str(jaccard(tt, all_mg, 1, "", 'with'))
    after_jaccard = str(jaccard(tt, all_mg, 2, alg, 'with'))
    before_f_score = f_score(before_precision, before_recall)
    after_f_score = f_score(after_precision, after_recall)
    movie_json["before"] = {"precision": before_precision, "recall": before_recall, "jaccard": before_jaccard,
                            "fscore": before_f_score}
    movie_json["after"] = {"precision": after_precision, "recall": after_recall, "jaccard": after_jaccard,
                           "fscore": after_f_score}
    return movie_json


def extract_movie_results_to_json(tt, movie_name):
    full_json = {}
    base_path = Path(__file__).parent.parent.parent
    movie_path = base_path / "vi_json/{}.json".format(tt)
    alg1 = algorithm_1(movie_path, create_faces_list(movie_path))
    alg2 = algorithm_2_improved(movie_path, create_faces_list(movie_path))
    alg3 = algorithm_faces_speakers(movie_path, create_faces_list(movie_path))
    alg4 = pipeline_algorithm([algorithm_faces_speakers, algorithm_2_improved, algorithm_1], movie_path)
    full_json["algo1"] = get_data(tt, alg1)
    full_json["algo2"] = get_data(tt, alg2)
    full_json["algo3"] = get_data(tt, alg3)
    full_json["algo4"] = get_data(tt, alg4)
    with open('extracted_' + movie_name + '.json', 'w') as outfile:
        json.dump(full_json, outfile)



if __name__ == '__main__':
    # print(get_insight('tt0988595', dress_27, 1))
    print_pretty_changes_algorithm('with', 1)
# print_pretty_changes_algorithm('without', 1)


# print_pretty_changes_algorithm('with', 2)
# print_pretty_changes_algorithm('without', 2)

# print_pretty_changes_algorithm('with', 3)
# print_pretty_changes_algorithm('without', 3)

# print_pretty_changes_algorithm('with', 4)
# print_pretty_changes_algorithm('without', 4)

# print_pretty_changes_algorithm('with', 5)
# print_pretty_changes_algorithm('without', 5)
"""
print_pretty_changes_algorithm('with', 6)
print_pretty_changes_algorithm('without', 6)

print_pretty_differences('tt0988595', 'with')
print_pretty_differences_test('tt0988595')
"""
