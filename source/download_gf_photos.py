import argparse
import json
import sys
import os
import urllib.request

def download_photos(photos_file, folder_name):
	photos = json.load(open(photos_file))

	for girl in photos:
		girl_folder = folder_name + '/' + girl['domain']
		os.makedirs(girl_folder, exist_ok=True)

		for photo in girl['photos']:
			photo_url = None

			if 'url_small' in photo:
				photo_url = photo['url_small']
			elif 'url_big' in photo:
				photo_url = photo['url_big']
			else:
				continue

			photo_name = str(photo['id']) + '.jpg'
			photo_path = girl_folder + '/' + photo_name

			if os.path.exists(photo_path):
				continue

			try:
				urllib.request.urlretrieve(photo_url, photo_path)
			except (KeyboardInterrupt, SystemExit):
				raise
			except:
				print("Can't download photo: " + photo_url, file=sys.stderr)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Download gf photos')
	parser.add_argument('json', help='json array with photos (check exmape/photos_list_exampe.json for format)')
	parser.add_argument('folder_name')
	args = parser.parse_args()

	download_photos(args.json, args.folder_name)