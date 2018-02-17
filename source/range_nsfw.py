import os
import json
import argparse
import subprocess

def range_nswf(folder, json_path, result_path):
    scores = sorted_scores(range_nsfw_folder_and_merge_with_json(folder, json_path))
    os.makedirs(os.path.dirname(result_path), exist_ok=True)

    result_path = result_path + '.json'
    f = open(result_path, 'w')
    f.write(json.dumps(scores))
    f.close()

    return result_path

def range_nsfw_folder_and_merge_with_json(folder, json_path):
    scores = range_nsfw_folder(folder)
    user_json = json.load(open(json_path))

    for score in scores:
        user = list(filter(lambda json_user: json_user['domain'] == score['user_id'],  user_json))[0]
        photo = list(filter(lambda photo: photo['id'] == score['photo_id'], user['photos']))[0]
        score['img_url'] = photo['url_big']  if 'url_big' in photo else photo['url_small']
        score['name'] = user['first_name'] + ' ' + user['last_name']
        score['likes_count'] = photo['likes_count']

    return scores


def range_nsfw_folder(folder):
    run_command = 'docker run --volume=$(pwd):/workspace bvlc/caffe:cpu \
                    python source/open_nsfw/classify_nsfw.py \
                    --model_def source/open_nsfw/nsfw_model/deploy.prototxt \
                    --pretrained_model source/open_nsfw/nsfw_model/resnet_50_1by2_nsfw.caffemodel ' + folder + ' 2>/dev/null'

    scores = subprocess.getoutput(run_command).split('\n')

    result = []

    for score in scores:
        nsfw_score = score.split('\t')[0].split(':')[1]
        user_id = score.split('\t')[1].split('/')[-2]
        photo_id = score.split('\t')[1].split('/')[-1].split('.')[0]

        result.append({
            'user_id' : user_id,
            'photo_id' : int(photo_id),
            'score' : float(nsfw_score)
        })

    return result

def sorted_scores(scores):
    return sorted(scores, key=lambda photo: photo['score'], reverse=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Range nsfw images')
    parser.add_argument('folder', help='folder with images to range')
    parser.add_argument('json_path', help='path to json file with photos')
    parser.add_argument('result_path', help='path to result file without extension')
    args = parser.parse_args()

    range_nswf(args.folder, args.json_path, args.result_path)
