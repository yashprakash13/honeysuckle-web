import json
import os
import pickle
import time

import AO3
import requests
from bs4 import BeautifulSoup

from .constants import AO3_HARMONY_FEED_URL, FEEDDATA


class FeedMaker:
    def __init__(self, refresh=False):
        self.feeddict = []
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
        self._parse_ao3()

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
        """scrape and get works from 1st page of ao3 Harmony relationship tag and save to file"""

        html = requests.get(AO3_HARMONY_FEED_URL).content
        soup = BeautifulSoup(html, "html.parser")
        all_stories_ol = soup.find("ol", {"class": "work index group"}).findAll("li", recursive=False)
        a = time.time()
        print("Making AO3 harmony first page feed.")
        for li in all_stories_ol:
            workid = li.get("id")[5:]
            work = AO3.Work(int(workid))
            work = self._get_work_dict(work)
            self.feeddict.append(work)
        print("AO3 harmony first page feed made. Time taken: ", round(time.time() - a, 1))

        # save the feed fetched
        with open(os.path.join(FEEDDATA, "ao3feeddata"), "w") as fout:
            json.dump(self.feeddict, fout)

    def _get_work_dict(self, work):
        """get work elements from a work object of AO3 api class"""
        author_names_list = []
        for author in work.authors:
            author_names_list.append(author.username)
        workdict = {
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
