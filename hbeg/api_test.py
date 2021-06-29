import requests
import json
import ast

def get_story_details(link):
    story_id = link[link.index('s/')+2 : link.index('/', link.index('s/')+4)]

    response = requests.get(f'http://localhost:8000/hsapi/ffn/{story_id}')
    data = json.loads(response.text)
    
    print(data['title'])


get_story_details('https://www.fanfiction.net/s/2963991/1/Harry-Potter-and-the-Oroborus-Light')