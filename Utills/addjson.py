import json
import ntpath
import os
from pathlib import Path
from BussinesLayer.Data.data import check_attributes_exists, manage_config


def add_json():
    base_path = Path(__file__).parent.parent
    file_path = (base_path / "BussinesLayer/Algorithms/Visualize/vi_json/").resolve()
    directory = file_path
    path_list = Path(directory).glob('*.json')
    for path in path_list:
        with open(path) as json_file:
            data = json.load(json_file)
            print(data['name'])
            head, tail = ntpath.split(path)
            print(os.path.splitext(tail)[0])
            # add_new_video("aaaa", data['name'], os.path.splitext(tail)[0])


if __name__ == '__main__':
    s = manage_config()
    print(check_attributes_exists(s))
