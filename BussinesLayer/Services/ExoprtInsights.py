from BussinesLayer.Services.APIconnection import get_info_json_from_video, export_json_to_file


def export_json_of_video_to_file(video_id, name):
    json_data = get_info_json_from_video(video_id)
    export_json_to_file(json_data, name)
