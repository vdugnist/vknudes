import urllib.request
import urllib.parse
import argparse
import json

vk_api_version = '5.71'

def get_user_screen_name(access_token):
	parameters = {'v' : vk_api_version, 'access_token' : access_token}
	url = 'https://api.vk.com/method/account.getProfileInfo?' + urllib.parse.urlencode(parameters)
	res_body = urllib.request.urlopen(url).read()
	res_json = json.loads(res_body.decode("utf-8"))

	if 'response' not in res_json:
		print(res_json)
		sys.exit(1)

	return res_json['response']['screen_name']

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Get vk name')
	parser.add_argument('token',  help='vk oauth access token')
	args = parser.parse_args()
	
	print(get_user_screen_name(args.token))
