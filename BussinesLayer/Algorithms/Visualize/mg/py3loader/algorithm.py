from BussinesLayer.Data.data import extract_actors


def create_faces_list(json):
    faces = extract_actors(json)
    objects = []
    for face in faces:
        instances = face["instances"]
        for inst in instances:
            pair = (inst["start"], inst["end"], face["name"])
            objects.append(pair)
    return sorted(objects)


def algorithm_1(json):
    data = create_faces_list(json)
    result = []
    for idx, (start, end, name) in enumerate(data):
        if "Unknown" in name:
            if idx < len(data) - 1 and idx > 0:
                (s1, e1, name_before) = data[idx - 1]
                (s2, e2, name_after) = data[idx + 1]
                if 'Unknown' not in name_before and name_before == name_after:
                    if e1 > start or end > s2:
                        result.append((start, end, name))
                    else:
                        #print(s1, e1)
                        result.append((start, end, name_after))
                        #print("start:"+start+". end: "+end + ". name before:" + name_before +
                        #  ". name middle:" + name + ". name after:" + name_after)
                        #print(s2, e2)
                else:
                    result.append((start, end, name))
            else:
                result.append((start, end, name))
        else:
            result.append((start, end, name))
    return result
