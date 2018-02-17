import urllib.request
import urllib.parse
import argparse
import json
import time
import sys
import os

vk_api_version = '5.71'
top_liked_count = 100
vk_api_sleep_delay = 0.33

def get_gf_photos_and_save_to_folder(access_token, folder, screen_name, should_reload=False):
	os.makedirs(folder, exist_ok=True)

	filename = folder + '/' + screen_name + '.json'

	if os.path.isfile(filename) and not should_reload:
		return filename

	result = get_gf_photos_json(access_token)

	f = open(filename, 'w')
	f.write(result)
	f.close()

	return filename

def get_gf_photos_json(access_token):
	photos_list = append_gf_photos_to_photos_list(access_token, get_gf_list(access_token))
	return json.dumps(photos_list)


def get_gf_list(access_token):
	default_parameters = {'v' : vk_api_version, 'access_token' : access_token}
	request_parameters = {'fields' : 'sex,domain'}
	parameters = {**request_parameters, **default_parameters}
	url = 'https://api.vk.com/method/friends.get?' + urllib.parse.urlencode(parameters)
	
	res_body = urllib.request.urlopen(url).read()
	friends_list = json.loads(res_body.decode("utf-8"))

	gf_list = []

	for friend in friends_list['response']['items']:
		if friend['sex'] == 1 and 'deactivated' not in friend:
			gf_list.append(friend)

	return gf_list


def append_gf_photos_to_photos_list(access_token, gf_list):
	for gf in gf_list:
		photos = get_gf_photos(access_token, gf['id'])
		gf['photos'] = photos
	
	return gf_list


def get_gf_photos(access_token, gf_id):
	offset = 0
	count = 200
	photos = []
	has_more_photos = True

	while has_more_photos:
		default_parameters = {'v' : vk_api_version, 
							  'access_token' : access_token}
		request_parameters = {'owner_id' : gf_id, 
							  'count' : count, 
							  'offset' : offset, 
							  'photo_sizes' : 1, 
							  'extended' : 1}
		parameters = {**request_parameters, **default_parameters}
		url = 'https://api.vk.com/method/photos.getAll?' + urllib.parse.urlencode(parameters)
		
		res_body = urllib.request.urlopen(url).read()
		res_json = json.loads(res_body.decode("utf-8"))

		if 'response' not in res_json:
			print(res_json)
			sys.exit(1)

		formatted_photos = convert_photos(res_json['response']['items'])
		photos.extend(formatted_photos)
		offset += count
		has_more_photos = offset < res_json['response']['count']
		time.sleep(vk_api_sleep_delay)

	return filtered_gf_photos(photos)


def convert_photos(photos):
	result = []

	for photo in photos:
		formatted_photo = {}
		formatted_photo['id'] = photo['id']
		formatted_photo['likes_count'] = photo['likes']['count']

		for size in photo['sizes']:
			if size['type'] == 'r':
				formatted_photo['url_small'] = size['src']
			elif size['type'] == 'z':
				formatted_photo['url_big'] = size['src']
			elif size['type'] == 'y' and 'url_big' not in formatted_photo:
				formatted_photo['url_big'] = size['src']

		result.append(formatted_photo)

	return result


def filtered_gf_photos(gf_photos):
	return sorted(gf_photos, key=lambda photo: photo['likes_count'], reverse=True)[:top_liked_count]


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Download gf photos json')
	parser.add_argument('token',  help='vk oauth access token')
	parser.add_argument('folder', help='folder to save json')
	parser.add_argument('filename', help='filename without extension')
	args = parser.parse_args()

	print(get_gf_photos_and_save_to_folder(args.token, args.folder, args.filename, should_reload=True))
