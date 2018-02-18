# VKnudes

## Requirements
- python3
- docker

## Setup
```
git submodule update --init
docker pull bvlc/caffe:cpu  
pip3 install django
```

## Usage
`python3 vknudes.py {vk_token}`

## How to get vk_token
- Open [link](https://oauth.vk.com/authorize?client_id=6348349&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,photos&response_type=token&v=5.71)
- Accept auth
- Copy access_token parameter from redirected url

