import argparse
import datetime
import subprocess

from source import get_vk_id
from source import get_gf_photos_json
from source import download_gf_photos
from source import range_nsfw
from source import generate_html

def timed_print(message):
    print(str(datetime.datetime.now().time()) + ": " + message)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='show your hottest gfs')
    parser.add_argument('token', help='vk token')
    token = parser.parse_args().token


    vk_json_folder = 'vk_jsons'
    photos_folder = 'photos'
    nsfw_scores_folder = 'nsfw_scores'
    html_folder = 'html_result'

    timed_print('getting vk name')
    vk_name = get_vk_id.get_user_screen_name(token)

    timed_print('getting vk photos json')
    vk_json_path = get_gf_photos_json.get_gf_photos_and_save_to_folder(token, vk_json_folder, vk_name)

    current_user_photos_folder = photos_folder + '/' + vk_name
    timed_print('downloading user photos')
    download_gf_photos.download_photos(vk_json_path, current_user_photos_folder)

    current_user_nsfw_scores_file = nsfw_scores_folder + '/' + vk_name
    timed_print('scoring nsfw')
    scored_json_path = range_nsfw.range_nswf(current_user_photos_folder, vk_json_path, current_user_nsfw_scores_file)

    html_result_path = html_folder + '/' + vk_name + '.html'
    timed_print('generating html')
    generate_html.generate_html_and_save(scored_json_path, html_result_path)

    subprocess.run(['open', html_result_path])
