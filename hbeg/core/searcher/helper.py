import os
import time
import ast
import pickle5 as pickle

import pandas as pd
import numpy as np
from rapidfuzz import process, fuzz
import whoosh.index as windex
from whoosh.index import create_in
from whoosh.fields import *
from whoosh import qparser
from whoosh.qparser import QueryParser, MultifieldParser
# import faiss
# from sentence_transformers import SentenceTransformer
import stopwords
stop = stopwords.get_stopwords("en")
stop.extend(['Harry', 'Potter'])
stop = [word.lower() for word in stop]

# import constants here
from .constants import *

# the Data class
class Data:
    def __init__(self, pairs):
        self.pairs = pairs
        self.data = {}
        self.data_una = {}
        self.df = pd.read_csv(MAIN_EN_DATA_PATH, low_memory=False)
    
    def _get_ids_una_per_row(self, row, chars_present, list_to_append_to):
        if str(row['characters']) != 'NoCharacters' and set(chars_present).issubset(ast.literal_eval(str(row['characters']))):
            list_to_append_to.append(row['story_id'])
        
    def _load_una_ids(self, pair):
        una_list = []
        self.data['NoPairs'].apply(lambda row: self._get_ids_una_per_row(row, PAIR_CHARACTER_MAPPING[pair], una_list), axis=1)
        self.data_una[pair] = una_list
    
    def load_una_ids(self):
        print('Loading una ids.')
        for pair in PAIRS_TO_CALC_UNA_FOR:
            self._load_una_ids(pair)
        print('All una ids loaded.')
        
    def _load_data(self, pair):
        df = self.df[self.df.Pairs.str.contains(pair)]
        self.data[pair] = df
    
    def load_data(self):
        print('Loading data.')
        self.df['title_without_stopwords'] = self.df['title'] \
                        .apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in (stop)]))
        for pair in self.pairs:
            self._load_data(pair)
        print('All data loaded.')


# Indices class
class Indices(Data):
    def __init__(self, pairs=PAIRS_TO_LOOK_FOR):
        Data.__init__(self, pairs)
        self.psieindices = {}
        self.sieindex = None
        self.sie_ids = None
        Data.load_data(self)
        # Data.load_una_ids(self)
    
    
    def _load_psieindex(self, pair):
        ix = windex.open_dir(os.path.join(PSIE_INDEX_PATH, pair.lower()))
        self.psieindices[pair] = ix
        
    
    def _make_psieindex(self, pair, load_or_not=False):
        schema = Schema(story_id = ID(stored=True), summary = TEXT)
        if not os.path.exists(os.path.join(PSIE_INDEX_PATH, pair.lower())):
            os.mkdir(os.path.join(PSIE_INDEX_PATH, pair.lower())) 
        else:
            print(f'Index already exists for: {pair}')
            return
        ix = create_in(os.path.join(PSIE_INDEX_PATH, pair.lower()), schema) 
        if load_or_not:
            self.psieindices.append(ix)
        
        df_pair = self.data[pair]
        id_list = df_pair.story_id.to_list()
        summary_list = df_pair.summary.to_list()
        
        writer = ix.writer()
        for i in range(0, len(id_list)):
            writer.add_document(story_id = str(id_list[i]), 
                                summary = str(summary_list[i]))
        writer.commit() 
        print(f'Index made for: {pair}')
        
    
    def make_psieindices(self, load_or_not=False):
        for pair in self.pairs:
            self._make_psieindex(pair, load_or_not)
    
    
    def load_psieindices(self):
        print('Loading psie indices.')
        for pair in self.pairs:
            self._load_psieindex(pair)
        print('Loaded psie indices. ')
    
    
    def _load_sie_ids(self):
        embed_tuple = self._read_sie_tuple()
        self.sie_ids = embed_tuple[0]
    
    
    def _read_sie_tuple(self):
        with open(os.path.join(SIE_EMBED_PATH, SIE_EMBED_NAME), 'rb') as f:
            embed_tuple = pickle.load(f)
        return embed_tuple
    
    
    def _make_sieindex(self):
        # read the embed file
        embed_tuple = self._read_sie_tuple()
        
        # get the embeddings list
        embed = embed_tuple[1]
        
        # faiss quantizer
        quantizer = faiss.IndexFlatL2(DIMENSION)
        #define a new inverted index 
        index = faiss.IndexIVFPQ(quantizer, DIMENSION, NLIST, M, BYTES)

        # train and then add data to index
        index.train(embed)
        index.add(embed)

        # save to disk
        faiss.write_index(index, os.path.join(SIE_INDEX_PATH, SIE_INDEX_NAME))

        
    def make_sieindex(self):
        if os.path.exists(os.path.join(SIE_INDEX_PATH, SIE_INDEX_NAME)):
            print('sie index already present.')
            return
        print('sie index not found. Making one.')
        self._make_sieindex()
        print('Made sie index.')
    
    
    def  _load_sieindex(self):
        self.sieindex = faiss.read_index(os.path.join(SIE_INDEX_PATH, SIE_INDEX_NAME))
    
    
    def load_sieindex(self):
        print('Loading sie index.')
        self._load_sieindex()
        self._load_sie_ids()
        print('Loaded sie index.')