def getTop5PerScene(pathfile):
    file = open(pathfile, "r")
    rows = 0
    counts = []
    for line in file:
        line = line.rstrip()
        if line.isnumeric():
            counts.append(int(line))
            rows = int(line)
    col = max(set(counts), key=counts.count) * 5 + 100
    result = [[0] * col for i in range(rows)]
    file.close()
    file = open(pathfile, "r")
    i = 0
    j = 0
    for line in file:
        line = line.rstrip()
        if line.isnumeric():
            if i != int(line) - 1:
                j = 0
            i = int(line) - 1
        elif "Top 5 actions" in line or line == "":
            continue
        elif "***" in line or "[[" in line:
            continue
        else:
            splits = line.split(":")
            action = splits[0].strip()
            if 'nan' not in splits[1].strip():
                percentage = float(splits[1].strip().strip('%'))
            result[i][j] = (action, percentage)
            j = j + 1
    return result


def checkExistance(element, list):
    for elem in list:
        if element != 0 and element[0] == elem[0]:
            return False
    return True


def unionAction(scene_):
    result = []
    for element in scene_:
        for elementResult in result:
            if element != 0 and element[0] in elementResult[0]:
                temp = list(elementResult)
                temp[1] = temp[1] + element[1]
                if temp[1] > 100:
                    temp[1] = 100
                result.remove(elementResult)
                result.append(tuple(temp))
        if checkExistance(element, result):
            result.append(element)
    return result


def unionIdenticalAction(list):
    full_movie = []
    for scene in list:
        specific_scene = unionAction(scene)
        full_movie.append(specific_scene)
    return full_movie


def fix(scene):
    new_scene = []
    for element in scene:
        if element != 0:
            new_scene.append(element)
    return new_scene


def get_clean_results(path):
    total_result = []
    top5 = getTop5PerScene(path)
    results = unionIdenticalAction(top5)
    for scene in results:
        fixed_scene = fix(scene)
        total_result.append(fixed_scene)
    return total_result


if __name__ == '__main__':
    s = get_clean_results('./test.txt')
    for i in s:
        print(i)
    # print(s)
