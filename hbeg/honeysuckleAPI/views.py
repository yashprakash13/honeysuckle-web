import json
from datetime import date, datetime

import requests
from core.searcher import utils
from core.searcher.constants import COLS_TO_SEND_BY_HS_API

# import the searcher instance from core app
from core.views import instance
from django.shortcuts import render
from profiles.models import Story
from rest_framework.response import Response
from rest_framework.views import APIView
from sections.harmony.models import (
    WEBSITE_CHOICES,
    HarmonyFicsBlacklist,
    HarmonyTropesModel,
)

from .api import *


class GetStoryDetailsFfn(APIView):
    """View to get story meta from ffn"""

    def get(self, request, story_id):
        print("Got:", story_id)

        story_all_fields = execute_ffn_search_and_response(story_id)

        # prepare the API response with story details
        story = {
            "link": story_all_fields["link"],
            "thumb_image": story_all_fields["story_image"],
        }
        for key in COLS_TO_SEND_BY_HS_API:
            story[key] = story_all_fields[key]

        # save the story or not, check and save here if needed
        initiate_save_story(story_all_fields)

        # if story gotten, return it as a response
        if story:
            del story["story_id"]
            return Response(story)
        else:
            return Response("Not found.")


class GetStoryDetailsAo3(APIView):
    """View to get story meta from ao3"""

    def get(self, request, story_id):
        url = f"https://archiveofourown.org/works/{story_id}"
        print(f"Trying url from Ao3 API: {url}")
        story = get_story_details_from_response_ao3(story_id)
        story["link"] = url

        story["date_published"] = get_story_dates_cleaned_ao3(story["date_published"], False)
        story["date_updated"] = get_story_dates_cleaned_ao3(story["date_updated"], False)

        return Response(story)


class BlacklistView(APIView):
    """View to get all blacklisted fics"""

    def get(self, request):
        all_stories_ffn = HarmonyFicsBlacklist.objects.filter(website__in=(WEBSITE_CHOICES[0])).values_list(
            "id", "author_name", "story_name", "votes"
        )
        all_stories_ao3 = HarmonyFicsBlacklist.objects.filter(website__in=(WEBSITE_CHOICES[1])).values_list(
            "id", "author_name", "story_name", "votes"
        )

        response = {"all_stories_ffn": all_stories_ffn, "all_stories_ao3": all_stories_ao3}

        return Response(response)


class CreateOrAddBlacklistFic(APIView):
    """View to create or add votes to a blacklisted fic"""

    def get(self, request, story_id):

        if "FFN" in story_id:
            choice = WEBSITE_CHOICES[0]
        elif "AO3" in story_id:
            choice = WEBSITE_CHOICES[1]
        elif "ID" in story_id:
            story_id = int(story_id[2:])
            print("ID got= ", story_id)
            # story exists, so add a vote
            try:
                obj = HarmonyFicsBlacklist.objects.get(id=story_id)
                obj.votes = obj.votes + 1
                obj.save()
                return Response({"resp": "200_VOTE_ADDED"})
            except:
                return Response({"resp": "404_WRONG_URL"})
        else:
            return Response({"resp": "404_WRONG_URL"})

        story_id = story_id[3:]
        if HarmonyFicsBlacklist.objects.filter(storyid=story_id).exists():
            # story exists, so add a vote
            obj = HarmonyFicsBlacklist.objects.get(storyid=story_id)
            obj.votes = obj.votes + 1
            obj.save()
            return Response({"resp": "200_VOTE_ADDED"})
        else:
            # story doesn't exist, so add it
            if choice == WEBSITE_CHOICES[0]:
                # FFN
                story_all_fields = execute_ffn_search_and_response(story_id)
                HarmonyFicsBlacklist.objects.create(
                    storyid=story_id,
                    website=choice[0],
                    votes=1,
                    story_name=story_all_fields["title"],
                    author_name=story_all_fields["author_name"],
                )
            else:
                # AO3
                story_all_fields = execute_ffn_search_and_response(story_id)
                HarmonyFicsBlacklist.objects.create(
                    storyid=story_id,
                    website=choice[0],
                    votes=1,
                    story_name=story_all_fields["title"],
                    author_name=story_all_fields["authors"],
                )
            return Response({"resp": "200_STORY_AND_VOTE_ADDED"})


# UTILITY CLASSES FOR SCRAPING ACTIONS---------------------------------------------------------------


def get_story_id_from_link(link):
    """
    just a helper func to get id from link ffn or ao3
    """

    if "fanfiction.net" in link:
        try:
            story_id = link[link.index("s/") + 2 : link.index("/", link.index("s/") + 4)]
        except:
            story_id = link[link.index("s/") + 2 :]
    elif "archiveofourown.org" in link:
        try:
            story_id = link[link.index("works/") + len("works/") : link.index("/", link.index("works/") + 6)]
        except:
            story_id = link[link.index("works/") + len("works/") :]
    else:
        story_id = None

    return story_id


def execute_ffn_search_and_response(story_id):
    """
    the main function to begin scraping ffn page from a story id
    """
    response = get_response_from_storyId_ffn(story_id)

    story_all_fields = get_all_story_metadata(story_id, response)

    return story_all_fields


def get_all_story_metadata(story_id, response):
    """
    get scraped metadata of story from api.py func
    """
    story_all_fields = get_story_details_from_reponse_ffn(story_id, response)
    story_all_fields["story_id"] = story_id

    return story_all_fields


def check_if_story_exists_in_csvdb(story_id):
    """
    to check if story does not exist in csv db
    """
    storygotten = instance.get_story_details(int(story_id))[COLS_TO_SEND_BY_HS_API]
    storygotten = storygotten.to_dict(orient="records")
    if len(storygotten) == 0:
        return False
    else:
        return True


def initiate_save_story(story_all_fields):
    """
    to check and store if story doesn't existg in csv db or discard if exists, given the story metadata
    """
    if (
        not check_if_story_exists_in_csvdb(story_all_fields["story_id"])
        and "Harry Potter" in story_all_fields["fandom"]
    ):
        story_all_fields["num_words"] = story_all_fields["num_words_to_store"]
        story_all_fields["characters"] = story_all_fields["characters_to_store"]
        story_all_fields["published"] = story_all_fields["published_to_store"]
        story_all_fields["updated"] = story_all_fields["updated_to_store"]
        story_all_fields["num_favs"] = story_all_fields["num_favs_to_store"]
        story_all_fields["num_follows"] = story_all_fields["num_follows_to_store"]
        story_all_fields["num_reviews"] = story_all_fields["num_reviews_to_store"]
        story_all_fields["genres"] = story_all_fields["genres_to_store"]

        # call the api.py func to save story into csv db
        save_new_story_into_csvdb(story_all_fields)

    else:
        print(f"Story {story_all_fields['story_id']} exists in csv db, or not of HP fandom.")
