import os
import json
import django
import argparse

from django.conf import settings
from django.template import loader

photos_count = 100

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': ['./source/templates'],
}]
settings.configure(TEMPLATES=TEMPLATES)
django.setup()

def generate_html_and_save(json_path, result_path):
    os.makedirs(os.path.dirname(result_path), exist_ok=True)
    html = generate_html(json_path)

    f = open(result_path, 'w')
    f.write(html)
    f.close()

def generate_html(json_path):
    photos = prepare_photos(json.load(open(json_path)))
    return loader.get_template('top_nsfw.html').render({'photos' : photos})

def prepare_photos(photos):
    return sorted(photos, key=lambda photo: photo['score'], reverse=True)[:photos_count]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate html from json')
    parser.add_argument('json_path', help='path to json')
    parser.add_argument('result_path', help='path to result html')
    args = parser.parse_args()

    generate_html_and_save(args.json_path, args.result_path)
