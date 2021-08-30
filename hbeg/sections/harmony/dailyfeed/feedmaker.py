import json
import os
import pickle
import time
from threading import Thread

import AO3
import pandas as pd
import requests
from bs4 import BeautifulSoup
from core.searcher.constants import NOT_AVAILABLE_AUTHOR_COL_ITEM
from core.searcher.utils import make_length
from core.views import instance

from .constants import AO3_HARMONY_FEED_URL, FEEDDATA


class FeedMaker:
    def __init__(self, refresh=False):
        self.feeddict = []
        self.df_ao3_hhr = None
        self.new_works_to_append = []
        # start making the feed
        if refresh:
            # called from the cron function
            self._refresh_feed()
        else:
            # called from view to fetch saved results or in worst case, make new feed and fetch
            self._make_feed()

    def _refresh_feed(self):
        """make new ao3 and ffn feed from 1st pages: this function is called by the scheduled cronjob"""

        # parse ao3 for new feed and save
        self.df_ao3_hhr = pd.read_csv(HHr_AO3_DATA_PATH)
        self._parse_ao3()
        self.df_ao3_hhr = None
        self.new_works_to_append = []

    def _make_feed(self):
        """make ao3 and ffn feed from 1st pages if not already present"""

        if os.path.exists(os.path.join(FEEDDATA, "ao3feeddata")):
            print("Found existing ao3 feed data. Loading...")
            with open(os.path.join(FEEDDATA, "ao3feeddata"), "r") as fin:
                self.feeddict = json.load(fin)
            print("Loaded existing ao3 feed data.")
        else:
            print("Not found ao3 feed data. Fetching...")
            self._parse_ao3()

    def get_feed(self):
        """return the feed list of work dicts"""

        return self.feeddict

    def _parse_ao3(self):
        """
        scrape and get works from 1st page of ao3 Harmony relationship tag and save to file,
        as well as update the csvdb with new works
        """

        html = requests.get(AO3_HARMONY_FEED_URL).content
        soup = BeautifulSoup(html, "html.parser")
        all_stories_ol = soup.find("ol", {"class": "work index group"}).findAll("li", recursive=False)
        a = time.time()
        print("Making AO3 harmony first page feed.")
        for li in all_stories_ol:
            workid = li.get("id")[5:]
            classtext = str(li.get("class"))
            try:
                author_id = classtext[classtext.index("user-") + 5 : classtext.index("]") - 1]
            except:
                author_id = NOT_AVAILABLE_AUTHOR_COL_ITEM

            # get work object with all metadata from ao3 api
            work = AO3.Work(int(workid))

            # check if story in existing csvdb, or append to dataframe to be inserted
            self._check_if_work_exists_in_csvdb(work, author_id)

            # get data to make the feed
            work = self._get_work_dict_for_feed(work)
            self.feeddict.append(work)
        print("AO3 harmony first page feed made. Time taken: ", round(time.time() - a, 1))

        # Add newly collected works to ao3 csvdb
        print("Adding new works to csvdb...")
        self._add_new_works_to_csvdb()
        print("Added new works to csvdb.")

        # reload data for searcher
        self._reload_data()

        # save the feed fetched
        with open(os.path.join(FEEDDATA, "ao3feeddata"), "w") as fout:
            json.dump(self.feeddict, fout)

    def _get_work_dict_for_feed(self, work):
        """get work elements from a work object of AO3 api class"""

        author_names_list = []
        for author in work.authors:
            author_names_list.append(author.username)
        workdict = {
            "story_id": work.id,
            "title": work.title,
            "authors": ", ".join(author_names_list),
            "categories": ", ".join(work.categories[:5]),
            "nchapters": work.nchapters,
            "characters": ", ".join(work.characters[:5]),
            "complete": work.complete,
            "language": work.language,
            "rating": work.rating,
            "relationships": ", ".join(work.relationships[:5]),
            "words": work.words,
            "tags": ", ".join(work.tags[:5]),
            "summary": work.summary,
        }
        return workdict

    def _check_if_work_exists_in_csvdb(self, work, author_id):
        """read the stored ao3 feed and get and store new HHr fics if not already present in csvdb"""

        if not int(work.id) in self.df_ao3_hhr.story_id.values:
            self._add_work_to_be_appended(work, author_id)

    def _add_work_to_be_appended(self, work, author_id):
        """get one full row of the new work to be appeneded"""

        author_names_list = []
        for author in work.authors:
            author_names_list.append(author.username)

        if work.complete:
            status = "Complete"
        else:
            status = "Incomplete"
        try:
            workdict = {
                "story_id": work.id,
                "title": work.title,
                "author_name": "!".join(author_names_list),
                "author_id": author_id,
                "num_chapters": work.nchapters,
                "characters": ", ".join(work.characters[:7]),  # THIS IS DIFF THAN FFNET
                "status": status,
                "language": work.language,
                "rated": work.rating,
                "num_words": work.words,
                "genres": "!".join(work.tags[:7]),
                "summary": work.summary,
                "updated": work.date_updated,
                "published": work.date_published,
                "Pairs": "Harmony",
                "Lengths": make_length(int(work.words)),
                # AO3 EXTRA FIELDS
                "categories": "!".join(work.categories[:7]),
                "num_kudos": work.kudos,
                "Medium": "AO3",
            }
            self.new_works_to_append.append(workdict)
        except Exception as e:
            print(e)

    def _add_new_works_to_csvdb(self):
        """save the new data to csvdb"""

        print("New works to append: ", pd.DataFrame(self.new_works_to_append).info())
        self.df_ao3_hhr = pd.concat([self.df_ao3_hhr, pd.DataFrame(self.new_works_to_append)])
        self.df_ao3_hhr.to_csv(HHr_AO3_DATA_PATH, index=False)

    def _reload_data(self):
        # load newly saved data in a background thread
        background_thread = Thread(target=instance.class_indices.load_temp_data)
        background_thread.start()
