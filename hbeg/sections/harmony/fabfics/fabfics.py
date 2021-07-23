"""
To utilise core.searcher's ffn searcher+db as well as ao3 + (a few others, in time) from here 
to deliver all HHr fics from a variety of websites
"""
import pandas as pd
from core.searcher.constants import COLS_TO_SHOW_STORY_DETAIL
from core.views import instance

from .constants import HHr_AO3_DATA_PATH


class HHrFicLoader:
    def __init__(self):
        self.ao3_data = pd.read_csv(HHr_AO3_DATA_PATH)
        self.ao3_fics = None
        self.ffn_fics = None
        self.authors = []
        print("Loading Harmony fics and authors...")
        self.load_fics_for_fics_page()
        self.load_authors_for_authors_page()
        print("Loaded Harmony fics and authors.")

    def load_fics_for_fics_page(self):
        """return fic list to display in Fics page"""
        self.ao3_fics = self.ao3_data[COLS_TO_SHOW_STORY_DETAIL]
        self.ao3_fics = self.ao3_fics.to_dict("records")

        self.ffn_fics = instance.class_indices.data["Harmony"]
        self.ffn_fics = self.ffn_fics.to_dict("records")

    def load_authors_for_authors_page(self):
        """return all authors list to display in authors page"""
        self.authors.extend(list(instance.class_indices.data["Harmony"].author_name.unique()))
        self.authors.extend(list(self.ao3_data.author_name.unique()))
        self.authors = list(set(self.authors))
