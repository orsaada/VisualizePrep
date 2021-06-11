from pathlib import Path

from BussinesLayer.Algorithms.Visualize.mg.py3loader.algorithm import create_faces_list, get_previous_face, \
    get_next_face, faces_shots_verification, map_face_to_speaker, get_speakers
from BussinesLayer.Data.data import extract_shots, extract_speakers_list_from_transcript_data


def algorithm_1_without_mg(json, faces_instances):
    result = []
    for idx, (start, end, name) in enumerate(faces_instances):
        if "Unknown" in name:
            if idx < len(faces_instances) - 1 and idx > 0:
                (s1, e1, name_before) = faces_instances[idx - 1]
                (s2, e2, name_after) = faces_instances[idx + 1]
                if 'Unknown' not in name_before and name_before == name_after:
                    if e1 > start or end > s2:  # overlap
                        continue
                    else:
                        result.append((start, end, 'Unknown', name_after))
                else:
                    continue
            else:
                continue
        else:
            continue
    return result


def algorithm_2_improved_without_mg(json, faces_instances):
    shots = extract_shots(json)
    result = []
    for idx, (start, end, name) in enumerate(faces_instances):
        if "Unknown" in name:
            if 0 < idx < len(faces_instances) - 1:
                (s1, e1, name_before) = get_previous_face(faces_instances, idx, start)
                (s2, e2, name_after) = get_next_face(faces_instances, idx, end)
                if 'Unknown' not in name_before and name_before == name_after and faces_shots_verification(shots, e1, start, end, s2):
                    result.append((start, end, 'Unknown', name_after))
                else:
                    continue
            else:
                continue
        else:
            continue
    return result


def algorithm_faces_speakers_without_mg(json, faces_instances):
    speakers_instances = extract_speakers_list_from_transcript_data(json)
    speakers_actors_mapping = map_face_to_speaker(speakers_instances, faces_instances)
    result = []
    for idx, (start, end, name) in enumerate(faces_instances):
        if "Unknown" in name:
            speakers = get_speakers(speakers_instances, start, end)
            speakers = list(dict.fromkeys(speakers))
            if len(speakers) == 1 and speakers[0] in speakers_actors_mapping:
                new_name = speakers_actors_mapping[speakers[0]]
                if 'Unknown' not in new_name:
                    result.append((start, end, "Unknown", new_name))
            else:
                continue
        else:
            continue
    return result


if __name__ == '__main__':
    base_path = Path(__file__).parent.parent.parent
    movie_path = base_path / "vi_json/{}.json".format('tt0073486')
    print(algorithm_1_without_mg(movie_path, create_faces_list(movie_path)))
