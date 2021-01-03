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
            if idx < len(data) - 1:
                (s1, e1, name_before) = data[idx - 1]
                (s2, e2, name_after) = data[idx + 1]
                if name_before == name_after:
                    result.append((start, end, name_after))
                else:
                    result.append((start, end, name))
            else:
                result.append((start, end, name))
        else:
            result.append((start, end, name))
    return result
