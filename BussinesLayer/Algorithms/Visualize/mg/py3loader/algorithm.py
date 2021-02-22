from BussinesLayer.Data.data import extract_actors,extract_shots,extract_speakers_list,extract_speakers_list_from_transcript_data
import itertools


def time_to_secs(t):
    l = t.split(':')
    return round(int(l[0])*3600 + int(l[1])*60 + float(l[2]), 2)


def create_faces_list(json):
    faces = extract_actors(json)
    objects = []
    for face in faces:
        instances = face["instances"]
        for inst in instances:
            pair = (inst["start"], inst["end"], face["name"])
            objects.append(pair)
    return sorted(objects)


def faces_in_same_shot_bool(shots, starttime_face_before, starttime_face_current, starttime_face_next):
    for (start, end) in shots:
        if face_in_shot_bool(start, end, starttime_face_before) & face_in_shot_bool(start, end, starttime_face_current)\
                and face_in_shot_bool(start, end, starttime_face_next):
            return True
    return False


def face_in_shot_bool(starttime_shot, endtime_shot, starttime_face):
    return starttime_shot <= starttime_face < endtime_shot


def get_previous_face(faces, curr_face_idx, curr_face_start_time):
    if curr_face_idx == 1:
        return faces[0]
    (s, e, name) = faces[curr_face_idx - 1]
    if curr_face_start_time >= e:
        return faces[curr_face_idx - 1]
    return get_previous_face(faces, curr_face_idx -1, curr_face_start_time)


def get_next_face(faces, curr_face_idx, curr_face_end_time):
    if curr_face_idx == len(faces) - 2:
        return faces[len(faces)-1]
    (s, e, name) = faces[curr_face_idx + 1]
    if curr_face_end_time <= s:
        return faces[curr_face_idx +1]
    return get_next_face(faces,curr_face_idx +1,curr_face_end_time)


'''
def check_face_recog_in_same_shot(json):
    shots = extract_shots(json)
    data = create_faces_list(json)

    for idx, (start, end, name) in enumerate(data):
        for idx2, (shot_start,shot_end) in enumerate(shots):
            if shot_start<= start < shot_end:
                if end>shot_end:
                    print(shot_start,start,shot_end,end,name)
'''





"""
verify if prev_face_start --- prev_face_end ---- cur_face_start --- cur_face_end --- next_face_start ---- next_face_end
                              [           same shot x          ]    [          same shot y          ]
shot x and shot y may be the same shot (x=y) or different shots 
the reason for the predicate is that face start time and end time bot always in a one shot 
in other words , face recognition instance can be spreads on more than one shot  
"""


def faces_shots_verification(shots, prev_face_end, cur_face_start, cur_face_end, next_face_start):
    for (shot_start, shot_end) in shots:
        if shot_start < prev_face_end <= cur_face_start < shot_end:
            for(shot_start_2, shot_end_2) in shots:
                if shot_start_2 < cur_face_end <= next_face_start < shot_end_2:
                    return True
            return False
    return False


def algorithm_2_improved(json,faces_instances):
    shots = extract_shots(json)
    #faces_instances = create_faces_list(json)
    result = []
    for idx, (start, end, name) in enumerate(faces_instances):
        if "Unknown" in name:
            if 0 < idx < len(faces_instances) - 1:
                (s1, e1, name_before) = get_previous_face(faces_instances,idx,start)
                (s2, e2, name_after) = get_next_face(faces_instances,idx,end)
                # predicate difference from algorithm2
                if 'Unknown' not in name_before and name_before == name_after and faces_shots_verification(shots, e1, start, end, s2):
                    result.append((start, end, name_after))
                    #print("start:"+start+". end: "+end + ". name before:" + name_before +
                    #". name middle:" + name + ". name after:" + name_after +"\n")
                else:
                    result.append((start, end, name))
            else:
                result.append((start, end, name))
        else:
            result.append((start, end, name))
    return result


#  Nati
def algorithm_2(json,faces_instances):
    shots = extract_shots(json)
    result = []
    for idx, (start, end, name) in enumerate(faces_instances):
        if "Unknown" in name:
            if 0 < idx < len(faces_instances) - 1:
                (s1, e1, name_before) = get_previous_face(faces_instances,idx,start)
                (s2, e2, name_after) = get_next_face(faces_instances,idx,end)
                if 'Unknown' not in name_before and name_before == name_after and faces_in_same_shot_bool(shots,e1,start,s2):
                    if e1 > start or end > s2:
                        result.append((start, end, name))
                    else:
                        result.append((start, end, name_after))
                else:
                    result.append((start, end, name))
            else:
                result.append((start, end, name))
        else:
            result.append((start, end, name))
    return result


def algorithm_1(json,faces_instances):
    result = []
    for idx, (start, end, name) in enumerate(faces_instances):
        if "Unknown" in name:
            if idx < len(faces_instances) - 1 and idx > 0:
                (s1, e1, name_before) = faces_instances[idx - 1]
                (s2, e2, name_after) = faces_instances[idx + 1]
                if 'Unknown' not in name_before and name_before == name_after:
                    if e1 > start or end > s2:  # overlap
                        result.append((start, end, name))
                    else:
                        result.append((start, end, name_after))
                        #print("start:"+start+". end: "+end + ". name before:" + name_before +
                        # ". name middle:" + name + ". name after:" + name_after)
                else:
                    result.append((start, end, name))
            else:
                result.append((start, end, name))
        else:
            result.append((start, end, name))
    return result


def map_face_to_speaker(speakers_instances,faces_instances):
    result = []
    for (speaker_start,speaker_end,speaker_id) in speakers_instances:
        faces = []
        for (face_start,face_end,name) in faces_instances:
            face_start_float = time_to_secs(face_start)
            face_end_float = time_to_secs(face_end)

            speaker_start_float = time_to_secs(str(speaker_start))
            speaker_end_float = time_to_secs(str(speaker_end))
            if face_start<=speaker_start<speaker_end<=face_end:
            # if 0<=abs(face_start_float - speaker_start_float)<=0.5 and 0<=abs(face_end_float - speaker_end_float)<=0.5 :
            # if speaker_start < face_start < speaker_end or speaker_start < face_end < speaker_end or
            # if  face_start<=speaker_start<speaker_end<=face_end:
            #   print(str(time_to_secs(face_end) - time_to_secs(face_start)))
            #   print([face_start,speaker_start,speaker_end,face_end])
                faces.append(name)
        #print([speaker_id,speaker_start,speaker_end,faces])
        result.append((str(speaker_id),faces))
    #print(sorted(result))
    key_f = lambda x: x[0]
    r = itertools.groupby(sorted(result), key_f)
    r2 = []
    for key, group in r:
       # print( key + ": " + str(list(group)))
        t = [lis[1] for lis in list(group)]

        r2.append((key,sorted([item for sublist in t for item in sublist])))
    #print(r2)
    mapping = []
    for (speaker_id,faces) in r2:
        if len(faces)>0:
            faces_grouping_counter = {i: faces.count(i) for i in faces}
            actor_speaker = max(faces_grouping_counter, key=faces_grouping_counter.get)
            #print ([speaker_id,actor_speaker])
            mapping.append((speaker_id,actor_speaker))

    return dict(mapping)


def get_speakers(speakers_instances, start, end):
    res = []
    for (speaker_start, speaker_end, speaker_id) in speakers_instances:
        if start <= speaker_start < end or start < speaker_end <= end:
            res.append(speaker_id)

    return res


def algorithm_faces_speakers(json, faces_instances):
    speakers_instances = extract_speakers_list_from_transcript_data(json)
    speakers_actors_mapping = map_face_to_speaker(speakers_instances, faces_instances)
    result = []
    for idx, (start, end, name) in enumerate(faces_instances):
        if "Unknown" in name:
            speakers = get_speakers(speakers_instances, start, end)
            #print(speakers)
            speakers =list(dict.fromkeys(speakers))
            if len(speakers) == 1 and speakers[0] in speakers_actors_mapping:

                new_name = speakers_actors_mapping[speakers[0]]
                #print(new_name)
                result.append((start, end, new_name))
            else:
                result.append((start, end, name))
        else:
            result.append((start, end, name))

    return result


def pipeline_algorithm(algorithms, json):
    res = create_faces_list(json)
    for algorithm in algorithms:
        res = algorithm(json, res)
    return res
