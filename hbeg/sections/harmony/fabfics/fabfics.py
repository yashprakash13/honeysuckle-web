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
        self.ao3_fics = None
        self.ffn_fics = None
        self.authors_ffn = []
        self.authors_ao3 = []
        print("Loading Harmony fics and authors...")
        self._load_fics_for_fics_page()
        print("Loaded Harmony fics and authors.")

    def _load_fics_for_fics_page(self):
        """return fic list and author list to display in Fics page"""

        self.ao3_fics = instance.get_all_harmony_ao3_fics()
        self.authors_ao3.extend(list(self.ao3_fics.author_name))
        self.ao3_fics = self.ao3_fics.to_dict("records")

        self.ffn_fics = instance.get_all_harmony_ffn_fics()
        self.authors_ffn.extend(list(zip(self.ffn_fics.author_id, self.ffn_fics.author_name)))
        self.ffn_fics = self.ffn_fics.to_dict("records")
