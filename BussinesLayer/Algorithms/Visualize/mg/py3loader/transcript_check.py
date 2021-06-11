import re
import json
from Levenshtein import distance as levenshtein_distance
from pathlib import Path
from sys import argv

# run with "python srttojson.py tt0455824.srt filename.json"
import textdistance


def parse_time(time_string):
    hours = int(re.findall(r'(\d+):\d+:\d+,\d+', time_string)[0])
    minutes = int(re.findall(r'\d+:(\d+):\d+,\d+', time_string)[0])
    seconds = int(re.findall(r'\d+:\d+:(\d+),\d+', time_string)[0])
    milliseconds = int(re.findall(r'\d+:\d+:\d+,(\d+)', time_string)[0])

    return (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds


def parse_srt_to_json(srt_string):
    srt_list = []

    for line in srt_string.split('\n\n'):
        if line != '':
            index = int(re.match(r'\d+', line).group())

            pos = re.search(r'\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+', line).end() + 1
            content = line[pos:]
            start_time_string = re.findall(r'(\d+:\d+:\d+,\d+) --> \d+:\d+:\d+,\d+', line)[0]
            end_time_string = re.findall(r'\d+:\d+:\d+,\d+ --> (\d+:\d+:\d+,\d+)', line)[0]
            start_time = parse_time(start_time_string)
            end_time = parse_time(end_time_string)

            srt_list.append({
                'index': index,
                'content': content,
                'start': start_time,
                'end': end_time
            })

    return srt_list


def extract_text_from_srt(srt_filename):
    srt = open(srt_filename, 'r', encoding='ISO-8859-1').read()
    text = ""

    for line in srt.split('\n\n'):
        if line != '':
            # index = int(re.match(r'\d+', line).group())

            pos = re.search(r'\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+', line).end() + 1
            content = line[pos:]
            # start_time_string = re.findall(r'(\d+:\d+:\d+,\d+) --> \d+:\d+:\d+,\d+', line)[0]
            # end_time_string = re.findall(r'\d+:\d+:\d+,\d+ --> (\d+:\d+:\d+,\d+)', line)[0]
            # start_time = parse_time(start_time_string)
            # end_time = parse_time(end_time_string)
            text = text + extract_text_from_srt_cont(content) + ' '

    return text


def extract_text_from_srt_cont(content):
    content2 = content.replace('<i>', ' ').replace('</i>', ' ').replace('#', ' ').replace('-', ' ')
    # remove all [] and their content
    pattern = r'\[.*?\]'
    text = re.sub(pattern, ' ', content2)
    return text


def extract_transcript_from_vi(json_path):
    with open(json_path, 'r', encoding="utf-8") as file:
        json_data = json.load(file)
    transcript = ''
    for i in json_data["videos"][0]["insights"]["transcript"]:
        transcript = transcript + i["text"] + ' '
    return transcript


def text_distance(vi_transcript, srt_text):
    levenshtein_similarity = 1 - levenshtein_distance(vi_transcript, srt_text) / max(len(vi_transcript), len(srt_text))
    # hamming_similarity = textdistance.hamming.normalized_similarity(vi_transcript, srt_text)
    jaccard_similarity = textdistance.jaccard.normalized_similarity(vi_transcript, srt_text)
    jaro_winkler_similarity = textdistance.jaro_winkler.normalized_similarity(vi_transcript, srt_text)
    cosine_similarity = textdistance.cosine.normalized_similarity(vi_transcript, srt_text)
    return [levenshtein_similarity, jaccard_similarity, jaro_winkler_similarity, cosine_similarity]


def test(json_path, srt_path):
    distance = (text_distance(extract_transcript_from_vi(json_path), extract_text_from_srt(srt_path)))
    return distance


# print(base_path)
# print(json_path)
# print(srt_path)
# print(type(extract_transcript_from_vi(json_path)))
# print(type(extract_text_from_srt(srt_path)))
# print(test(json_path, srt_path))

def run_all():
    base_path = Path(__file__).parent.parent.parent

    from os import listdir
    from os.path import isfile, join
    json_files = [f for f in listdir(base_path / "vi_json") if isfile(join(base_path / "vi_json", f))]
    for json_file in json_files:
        srt_file = json_file.replace("json", "srt")

        json_path = base_path / ("vi_json/" + json_file)
        srt_path = base_path / ("mg_srt/full_srt/" + srt_file)
        try:
            print((json_file, test(json_path, srt_path)))
        except:
            print("Something else went wrong")


def run_transcript(tt_movie):
    base_path = Path(__file__).parent.parent.parent.parent.parent.parent

    with open((base_path / 'config.json').resolve(), 'r') as f:
        data = json.load(f)
    tt_movie = data["ttMovie"]
    base_path = Path(__file__).parent.parent.parent
    json_path = base_path / ("vi_json/" + tt_movie + ".json")
    srt_path = base_path / ("mg_srt/full_srt/" + tt_movie + ".srt")
    return test(json_path, srt_path)


if __name__ == '__main__':
    run_transcript()
    # run_all()

# for js_file in json_path_list:
#    print(js_file)
#    print(1)
# srt_path_list = Path(srt_path).glob('*.srt')
# print(srt_path_list)
# for js_file in json_path_list:
#
#     print(js_file)
#     for srt_file in srt_path_list:
#         print(srt_file)
# print(test(json_path, srt_path))  # 20 times
# json_path =
# srt_path =
