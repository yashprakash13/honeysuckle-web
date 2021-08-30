import json

import requests

from .helper import *


# The Engine
class SearchEngine(Indices):
    def __init__(self):
        pass

    # API functions

    def search(self, query):
        response = requests.get("http://localhost:8080/search/", params={"query": query})
        response_list_of_dicts = eval(json.loads(response.text))
        return response_list_of_dicts

    def get_story_details(self, story_id):
        response = requests.get("http://localhost:8080/get_story_details/", params={"storyid": story_id})
        story_details = eval(json.loads(response.text))
        if story_details:
            return story_details[0]
        else:
            return []

    def save_story_into_csvdb(self, storydict, medium):
        # make the POST request
        data = {"storyid": storydict["story_id"], "medium": medium}
        response = requests.get("http://localhost:8080/save_new_story/", params=data)
        # print(response.text)
        # print(storydict)

    # MISC FUNCTIONS

    def get_story_link(self, story_id):
        return f"https://www.fanfiction.net/s/{story_id}"

    def get_story_link_ao3(self, story_id):
        return f"https://archiveofourown.org/works/{story_id}"

    # def get_story_details(self, story_id):
    #     df = self.class_indices.df
    #     return df.loc[df.story_id == story_id]

    # def get_all_harmony_ffn_fics(self):
    #     df = self.class_indices.df
    #     return df.loc[(df.Pairs == "Harmony") & (df.Medium == MEDIUM_FFN_COL_NAME)]

    # def get_all_harmony_ao3_fics(self):
    #     df = self.class_indices.df
    #     return df.loc[(df.Pairs == "Harmony") & (df.Medium == MEDIUM_AO3_COL_NAME)]
