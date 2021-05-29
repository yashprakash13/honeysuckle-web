# paths
MAIN_EN_DATA_PATH = 'data/en/metahp_nonullvalues_noduplicates_addedcols_touseforbackend_en.csv'
PSIE_INDEX_PATH = 'data/en_psie/indices'
SIE_INDEX_PATH = 'data/en_sie/index'
SIE_INDEX_NAME = 'sie_id_embedsumm_tuple_index'
SIE_EMBED_PATH = 'data/en_sie/embeds'
SIE_EMBED_NAME = 'id_summembed_tuple_en.pickle'
ST_MODEL_NAME = 'distilbert-base-nli-mean-tokens'

# search things
ALL_DF_COLUMNS = ['story_id', 'author_id', 'author_name', 'title',
                  'summary', 'updated', 'published', 'language',
                  'genres', 'rated', 'num_chapters', 'num_words',
                  'status', 'characters', 'num_reviews', 'num_favs',
                  'num_follows', 'Pairs', 'Lengths', 'title_without_stopwords'
                 ]
DEFAULT_PAIR = 'Harmony' # Yes, because that's MY ship. Period. 
PAIRS_TO_LOOK_FOR = ['Harmony', 'Haphne', 'Jily', 'Dramione', 'Tomione', 
                     'Volmione', 'Tomarry', 'Drarry', 'Jamione', 
                     'Snamione', 'Sirimione', 'Snarry', 'Remione',
                     'NoPairs', 'OtherPair'
                    ] # Volmione + Tomione is in one.
PAIRS_TO_CALC_UNA_FOR = ['Harmony', 'Jily', 'Haphne', 'Dramione', 'Tomione']
PAIR_CHARACTER_MAPPING = {
    'Harmony' : ['Harry P.', 'Hermione G.'],
    'Jily' : ['James P.', 'Lily Evans P.'],
    'Haphne' : ['Harry P.', 'Daphne G.'],
    'Dramione' : ['Draco M.', 'Hermione G.'],
    'Tomione' : ['Tom R. Jr.', 'Hermione G.']
}


ALL_LENGTHS = ['Small', 'Medium', 'Long', 'VeryLong']
SPECIAL_SEARCH_TOKENS = ['a:', 'l:']
AUTHOR_SEARCH_TOKEN = 'a:'
LENGTH_SEARCH_TOKEN = 'l:'

STANDARD_LENGTHS_TO_RETURN = 10
STANDARD_SCORE_CUTOFF = 75
NUM_MAX_RESULT_FETCH = 97
NUM_SUBSEQUENT_ROW_APPENDS = 3


# FAISS THINGS
M = 128
DIMENSION = 768
NLIST = 50  
BYTES = 8


# APP THINGS
COLS_TO_SHOW_STORY_DETAIL = ['story_id', 'title', 'author_name', 'rated', 
                            'summary', 'genres', 'num_chapters', 'num_words', 
                            'status', 'characters']