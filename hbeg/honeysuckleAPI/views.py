import requests
from datetime import datetime, date
import json

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from profiles.models import Story
# import the searcher instance from core app
from core.views import instance
from core.searcher.constants import COLS_TO_SEND_BY_HS_API, API_URL_TO_FETCH_STORIES_META_FROM
from core.searcher import utils

from .api import get_story_details_from_reponse, get_story_dates_cleaned, save_new_story_into_csvdb

class GetStoryDetailsFfn(APIView):
    def get(self, request, story_id):
        print('Got:', story_id)
    
        url = f"https://www.fanfiction.net/s/{story_id}"
        print(f'Trying url from Weaver API: {url}')
        response = requests.get(API_URL_TO_FETCH_STORIES_META_FROM,
                                params={'q': url},
                                data={'apiKey': 'example'},
                                auth=('weaver', '8D7RT-I;@m9LivXY3DA{Zik(2gmY')
                            )
        # get scraped metadata of story from api.py func
        story_all_fields = get_story_details_from_reponse(story_id, response)
        story_all_fields['story_id'] = story_id
        story_all_fields['link'] = url

        # prepare the API response with story details
        story = {'link':url}
        for key in COLS_TO_SEND_BY_HS_API:
            story[key] = story_all_fields[key]
            
        # save story fetched into csv db after checking if story does not exist in csv db
        storygotten = instance.get_story_details(int(story_id))[COLS_TO_SEND_BY_HS_API]
        storygotten = storygotten.to_dict(orient='records')
        if len(storygotten) == 0:
            story_all_fields['num_words'] = story_all_fields['num_words_to_store']
            story_all_fields['characters'] = story_all_fields['characters_to_store']
            story_all_fields['published'] = story_all_fields['published_to_store']
            story_all_fields['updated'] = story_all_fields['updated_to_store']
            story_all_fields['num_favs'] = story_all_fields['num_favs_to_store']
            story_all_fields['num_follows'] = story_all_fields['num_follows_to_store']
            story_all_fields['num_reviews'] = story_all_fields['num_reviews_to_store']
            story_all_fields['genres'] = story_all_fields['genres_to_store']

            save_new_story_into_csvdb(instance, story_all_fields)
        
        
        if story:
            del story['story_id']
            return Response(story)
        else:
            return Response('Not found.')