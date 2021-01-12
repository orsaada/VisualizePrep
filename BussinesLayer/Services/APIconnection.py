from video_indexer import VideoIndexer
import json
from BussinesLayer.Services.Logger import info


CONFIG = {
    'SUBSCRIPTION_KEY': '992fc8ddd8114d8f97048dc7efada7aa',
    'LOCATION': 'trial',
    'ACCOUNT_ID': 'ec3b46b9-654c-4465-9d74-1b7d5f8110c7'
}

# connect to Or Saada account
vi = VideoIndexer(
    vi_subscription_key=CONFIG['SUBSCRIPTION_KEY'],
    vi_location=CONFIG['LOCATION'],
    vi_account_id=CONFIG['ACCOUNT_ID']
)


# get info from data
def get_info_json_from_video(vid_id):  # get json of info from a video in indexer. return json object
    info("Video ID: " + vid_id + " - return json info")
    return vi.get_video_info(
        video_id=vid_id,
        video_language='English'
    )


# upload a video to video indexer - param1: path video, param2: future name in video indexer of video was upload
def upload_video(video_path, future_video_name):  # upload a video to video indexer. return video id
    info("Video Path: " + video_path + ", Video Name: " + future_video_name + " - was uploaded to video indexer")
    return vi.upload_to_video_indexer(
                input_filename=video_path,
                video_name=future_video_name,
                video_language='English'
        )


# export json(result) to exterior file
def export_json_to_file(json_file, future_filename):  # export json file
    info("Video Name: " + future_filename + " - was extracted to file")
    with open(future_filename+'.json', 'w', encoding='utf-8') as f:
        json.dump(json_file, f, ensure_ascii=False, indent=4)


def checkAPI():
    res = get_info_json_from_video("88ee0b48d8")
    print(res)


checkAPI()
