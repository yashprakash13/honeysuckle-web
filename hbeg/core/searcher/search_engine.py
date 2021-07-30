from .helper import *


def _append_df(df, dfs, num_appends=NUM_SUBSEQUENT_ROW_APPENDS):
    df0 = dfs[0]
    for df in dfs[1:]:
        df0 = df0.append(df.head(num_appends), ignore_index=True)
    return df0


pd.DataFrame._append_df = _append_df


# The Engine
class SearchEngine(Indices):
    def __init__(self):
        self.query_special_spl = None
        self.query = None
        self.query_spl = None
        self.author_search_word = None
        self.length_search_word = None
        self.df_to_use = None
        self.au_tokens_filt = None
        self.le_tokens_filt = None
        self.pairs_selected = None
        self.st_model = None
        self.psie_indices_filt = None
        self.is_phase_2 = False

        self.result_ids = None
        self.dym_title = None

    def _make_queries_and_load_model(self):
        """
        make searchable queries
        """
        query_full_spl = self.query.strip().split(" ")
        self.query_spl = [word for word in query_full_spl if word[:2] not in SPECIAL_SEARCH_TOKENS]

        self.query_special_spl = [word for word in query_full_spl if word[:2] in SPECIAL_SEARCH_TOKENS]
        self.query = " ".join(self.query_spl).strip()

        # self.st_model = SentenceTransformer(ST_MODEL_NAME)

    def _continuous_append(self, rows_appended, dfs):
        """
        to do continuous appends of result dfs (CA)
        """
        print(f"Inside CA func. Doing CA for {len(dfs)} dfs.")
        dftemp = pd.DataFrame(columns=ALL_DF_COLUMNS)
        while rows_appended <= NUM_MAX_RESULT_FETCH:
            for df in dfs:
                dftemp = dftemp.append(
                    df.iloc[rows_appended : rows_appended + NUM_SUBSEQUENT_ROW_APPENDS],
                    ignore_index=True,
                )
            rows_appended += NUM_SUBSEQUENT_ROW_APPENDS
        return dftemp

    def _select_rows_from_df(self, df, prop, category, num_rows=NUM_MAX_RESULT_FETCH):
        """
        to loc a particular num of rows with condition
        """
        return df.loc[df[prop] == category].head(num_rows)

    def _select_rows_from_df_simple(self, df, num_rows=NUM_MAX_RESULT_FETCH):
        """
        to iloc a particular num of rows with no condition
        """
        return df.iloc[:num_rows]

    def _order_rows_from_df(self, df, cat_property, cat_category, num_rows=None, ordered=True):
        """
        to iloc a particular num of rows with condition
        """
        if not num_rows:
            return df.iloc[(pd.Categorical(df[cat_property], categories=cat_category, ordered=ordered).argsort())]
        else:
            return df.iloc[
                (pd.Categorical(df[cat_property], categories=cat_category, ordered=ordered).argsort())
            ].head(num_rows)

    def _merge_res_dfs(self, dfdict):
        """
        merge multiple query result dfs smartly into one df
        """
        print(f"Inside the df merge func.{dfdict}")
        if self.df_to_use is not None:
            df = self.df_to_use
        else:
            df = self.class_indices.df

        df_to_return = pd.DataFrame(columns=ALL_DF_COLUMNS)
        rows_appended = 0

        # IF PHASE 2 INVOKED ----------------------------------------------------------------------------
        if self.is_phase_2:
            print("Inside phase 2 merge.")
            print("Result ids inside phase 2 merge: ", self.result_ids)

            dftemp = self._order_rows_from_df(df, "story_id", self.result_ids)

            if dfdict["div_2"]:
                dftemp2 = self._order_rows_from_df(df, "author_name", self.au_tokens_filt)
            if dfdict["div_3"]:
                dftemp3 = self._select_rows_from_df(dftemp, "Lengths", self.le_tokens_filt)
                if dfdict["div_2"]:
                    dftemp4 = self._select_rows_from_df(dftemp2, "Lengths", self.le_tokens_filt)

            # make resultant df
            df_to_return = df_to_return._append_df([dftemp.head(NUM_SUBSEQUENT_ROW_APPENDS)])
            if dfdict["div_2"]:
                df_to_return = df_to_return._append_df([dftemp2.head(NUM_SUBSEQUENT_ROW_APPENDS)])
            if dfdict["div_3"]:
                df_to_return = df_to_return._append_df([dftemp3.head(NUM_SUBSEQUENT_ROW_APPENDS)])
                if dfdict["div_2"]:
                    df_to_return = df_to_return._append_df([dftemp4.head(NUM_SUBSEQUENT_ROW_APPENDS)])

            # keep track of num rows appended and num rows left
            rows_appended += NUM_SUBSEQUENT_ROW_APPENDS
            # do CA
            if dfdict["div_2"]:
                df_to_return = df_to_return.append(self._continuous_append(rows_appended, [dftemp2]))
            if dfdict["div_3"]:
                df_to_return = df_to_return.append(self._continuous_append(rows_appended, [dftemp3]))
                if dfdict["div_2"]:
                    df_to_return = df_to_return.append(self._continuous_append(rows_appended, [dftemp4]))

            # remove duplicate rows appended
            df_to_return = df_to_return.drop_duplicates(subset=["story_id"])

            return df_to_return

        # PHASE 1 INVOKED -------------------------------------------------------------------------------------

        # Merge Rule 2 ---- all 4 divs--------------------------------------------------------------
        if dfdict["div_0"] and dfdict["div_1"] and dfdict["div_2"] and dfdict["div_3"]:
            print("Merge Rule 2 in effect.")
            # title or summary search (div_1) is already done on pair filtered df(div_0),
            # so only further filtering is needed for div_1 df on div_2 and div_3
            # filter with result ids for div1
            dftemp = self._order_rows_from_df(df, "story_id", self.result_ids)
            # filter with div2
            dftemp2 = self._order_rows_from_df(df, "author_name", self.au_tokens_filt)
            # filter with div3 for both previous dfs
            dftemp3 = self._select_rows_from_df(dftemp, "Lengths", self.le_tokens_filt)
            dftemp4 = self._select_rows_from_df(dftemp2, "Lengths", self.le_tokens_filt)
            # make resultant df
            df_to_return = df_to_return._append_df(
                [
                    dftemp2.head(NUM_SUBSEQUENT_ROW_APPENDS),
                    dftemp.head(NUM_SUBSEQUENT_ROW_APPENDS),
                    dftemp3.head(NUM_SUBSEQUENT_ROW_APPENDS),
                    dftemp4.head(NUM_SUBSEQUENT_ROW_APPENDS),
                ]
            )
            # keep track of num rows appended and num rows left
            rows_appended += NUM_SUBSEQUENT_ROW_APPENDS
            # do CA
            df_to_return = df_to_return.append(
                self._continuous_append(rows_appended, [dftemp2, dftemp, dftemp3, dftemp4])
            )
            # remove duplicate rows appended
            df_to_return = df_to_return.drop_duplicates(subset=["story_id"])

        # Merge Rule 3 -- any three divs-------------------------------------------------------------
        elif sum(val == True for val in dfdict.values()) == 3:
            print("Merge Rule 3 in effect.")
            # same procedure as Merge Rule 2
            # filter with result ids for div1
            if dfdict["div_1"] and not dfdict["div_2"]:
                dftemp = self._order_rows_from_df(df, "story_id", self.result_ids)
            # filter with div2
            elif not dfdict["div_1"] and dfdict["div_2"]:
                dftemp = self._order_rows_from_df(df, "author_name", self.au_tokens_filt)
            # filter with div3 for any of the previous dfs
            if dfdict["div_3"]:
                dftemp2 = self._select_rows_from_df(dftemp, "Lengths", self.le_tokens_filt)
            # make resultant df
            df_to_return = df_to_return._append_df(
                [
                    dftemp2.head(NUM_SUBSEQUENT_ROW_APPENDS),
                    dftemp.head(NUM_SUBSEQUENT_ROW_APPENDS),
                ]
            )
            # keep track of num rows appended and num rows left
            rows_appended += NUM_SUBSEQUENT_ROW_APPENDS
            # do CA
            df_to_return = df_to_return.append(self._continuous_append(rows_appended, [dftemp, dftemp2]))
            # remove duplicate rows appended
            df_to_return = df_to_return.drop_duplicates(subset=["story_id"])

        # Merge Rule 4 and 5
        else:
            # for any other combination or only 1 div--> rule 4 and 5
            print("Merge Rule 4 and 5 in effect.")

            # series of conditions for merge rule 5---------only 1 div present----------------------
            if dfdict["div_0"] and not dfdict["div_1"] and not dfdict["div_2"] and not dfdict["div_3"]:
                df_to_return = self._select_rows_from_df_simple(df)

            if dfdict["div_1"] and not dfdict["div_0"] and not dfdict["div_2"] and not dfdict["div_3"]:
                df_to_return = self._order_rows_from_df(df, "story_id", self.result_ids, NUM_MAX_RESULT_FETCH)

            if dfdict["div_2"] and not dfdict["div_0"] and not dfdict["div_1"] and not dfdict["div_3"]:
                df_to_return = self._order_rows_from_df(df, "author_name", self.au_tokens_filt, NUM_MAX_RESULT_FETCH)

            if dfdict["div_3"] and not dfdict["div_0"] and not dfdict["div_1"] and not dfdict["div_2"]:
                df_to_return = self._select_rows_from_df(df, "Lengths", self.le_tokens_filt)

            # series of conditions for merge rule 4 --------any 2 divs present---------------------
            if not dfdict["div_0"] and dfdict["div_1"] and dfdict["div_2"] and not dfdict["div_3"]:
                # filter with result ids for div1
                dftemp = self._order_rows_from_df(df, "story_id", self.result_ids)
                # filter with div2
                dftemp2 = self._order_rows_from_df(df, "author_name", self.au_tokens_filt)
                # make resultant df
                df_to_return = df_to_return._append_df(
                    [
                        dftemp2.head(NUM_SUBSEQUENT_ROW_APPENDS),
                        dftemp.head(NUM_SUBSEQUENT_ROW_APPENDS),
                    ]
                )
                # keep track of num rows appended and num rows left
                rows_appended += NUM_SUBSEQUENT_ROW_APPENDS
                # do CA
                df_to_return = df_to_return.append(self._continuous_append(rows_appended, [dftemp, dftemp2]))
                # remove duplicate rows appended
                df_to_return = df_to_return.drop_duplicates(subset=["story_id"])

            elif not dfdict["div_0"] and dfdict["div_1"] and not dfdict["div_2"] and dfdict["div_3"]:
                # filter with result ids for div1
                dftemp = self._order_rows_from_df(df, "story_id", self.result_ids)
                # filter for div3
                dftemp2 = self._order_rows_from_df(df, "Lengths", [self.le_tokens_filt])
                # make resultant df
                df_to_return = df_to_return._append_df(
                    [
                        dftemp2.head(NUM_SUBSEQUENT_ROW_APPENDS),
                        dftemp.head(NUM_SUBSEQUENT_ROW_APPENDS),
                    ]
                )
                # keep track of num rows appended and num rows left
                rows_appended += NUM_SUBSEQUENT_ROW_APPENDS
                # do CA
                df_to_return = df_to_return.append(self._continuous_append(rows_appended, [dftemp, dftemp2]))
                # remove duplicate rows appended
                df_to_return = df_to_return.drop_duplicates(subset=["story_id"])

            elif not dfdict["div_0"] and not dfdict["div_1"] and dfdict["div_2"] and dfdict["div_3"]:
                # filter with div2
                dftemp = self._order_rows_from_df(df, "author_name", self.au_tokens_filt)
                # filter for div3
                dftemp2 = self._order_rows_from_df(dftemp, "Lengths", [self.le_tokens_filt])
                # make resultant df
                df_to_return = df_to_return._append_df(
                    [
                        dftemp2.head(NUM_SUBSEQUENT_ROW_APPENDS),
                        dftemp.head(NUM_SUBSEQUENT_ROW_APPENDS),
                    ]
                )
                # keep track of num rows appended and num rows left
                rows_appended += NUM_SUBSEQUENT_ROW_APPENDS
                # do CA
                df_to_return = df_to_return.append(self._continuous_append(rows_appended, [dftemp, dftemp2]))
                # remove duplicate rows appended
                df_to_return = df_to_return.drop_duplicates(subset=["story_id"])

            elif dfdict["div_0"] and dfdict["div_1"] and not dfdict["div_2"] and not dfdict["div_3"]:
                df_to_return = self._order_rows_from_df(df, "story_id", self.result_ids, NUM_MAX_RESULT_FETCH)
            elif dfdict["div_0"] and not dfdict["div_1"] and dfdict["div_2"] and not dfdict["div_3"]:
                df_to_return = self._order_rows_from_df(df, "author_name", self.au_tokens_filt, NUM_MAX_RESULT_FETCH)
            elif dfdict["div_0"] and not dfdict["div_1"] and not dfdict["div_2"] and dfdict["div_3"]:
                df_to_return = self._select_rows_from_df(df, "Lengths", self.le_tokens_filt)

        return df_to_return

    def _return_res_ids(self, phase_one=True, query_to_search_empty=False):
        """
        results merge and return
        """
        print("Inside the return function.")
        df_dict = {"div_0": False, "div_1": False, "div_2": False, "div_3": False}

        if self.df_to_use is not None:
            print("Df to use is set. ")
            df_dict["div_0"] = True
        else:
            print("Using default df.")

        if phase_one:
            print("Inside phase 1 condition.")

            if self.dym_title:
                print(f"Did you mean {self.dym_title}")
            if self.result_ids:
                print("Title ids iloc operation.")
                df_dict["div_1"] = True

            if self.au_tokens_filt:
                print("au_tokens_filt is: ", self.au_tokens_filt)
                if query_to_search_empty:
                    print(f"Did you mean the author: {self.au_tokens_filt[0]}")
                df_dict["div_2"] = True

            if self.le_tokens_filt:
                print("le_tokens_filt is: ", self.le_tokens_filt)
                df_dict["div_3"] = True

        else:
            print("Inside phase 2 condition.")

            self.is_phase_2 = True

            if self.result_ids:
                print("Indices ids iloc operation.")
                df_dict["div_1"] = True

            if self.au_tokens_filt:
                print("au_tokens_filt is: ", self.au_tokens_filt)
                if query_to_search_empty:
                    print(f"Did you mean the author: {self.au_tokens_filt[0]}")
                df_dict["div_2"] = True

            if self.le_tokens_filt:
                print("le_tokens_filt is: ", self.le_tokens_filt)
                df_dict["div_3"] = True

        # merge dfs and return appropriately
        return self._merge_res_dfs(df_dict)

    def _title_search(self):
        """
        title search to be first done on the query
        """
        if self.df_to_use is not None:
            df = self.df_to_use
        else:
            df = self.class_indices.df

        res_r = process.extract(
            " ".join([word for word in self.query.split() if word.lower() not in (stop)]),
            df["title_without_stopwords"],
            scorer=fuzz.ratio,
            limit=STANDARD_LENGTHS_TO_RETURN,
            score_cutoff=STANDARD_SCORE_CUTOFF,
        )
        res_WR = process.extract(
            " ".join([word for word in self.query.split() if word.lower() not in (stop)]),
            df["title_without_stopwords"],
            scorer=fuzz.WRatio,
            limit=STANDARD_LENGTHS_TO_RETURN,
            score_cutoff=STANDARD_SCORE_CUTOFF,
        )

        # if no results
        if not res_r or not res_WR:
            return None, None

        if res_r[0][2] != res_WR[0][2]:
            # if WRatio and ratio return different top results, combine them
            index_list = [res_r[0][2], res_WR[0][2]]
        else:
            # Otherwise, just keep one of them
            index_list = [res_r[0][2]]

        # then, append all other results fetched too
        index_list.extend([r[2] for r in res_WR if r[2] not in index_list])
        index_list.extend([r[2] for r in res_r if r[2] not in index_list])

        story_ids_to_return = [df[df.index == i].story_id.item() for i in index_list]

        # Putting the 'Did you mean' thing here for title :)
        print("Title ids: ", story_ids_to_return)
        print("Index list for titles: ", index_list)
        if res_r[0][1] < 100:
            return (
                story_ids_to_return,
                df.loc[df["story_id"].isin(story_ids_to_return[:1])]["title"].item(),
            )
        else:
            return story_ids_to_return, None

    def _author_search(self):
        """
        search for author names
        """
        if self.df_to_use is not None:
            all_authors = self.df_to_use.author_name.unique()
        else:
            all_authors = self.class_indices.df.author_name.unique()

        res_r = process.extract(
            self.author_search_word,
            all_authors,
            scorer=fuzz.ratio,
            limit=STANDARD_LENGTHS_TO_RETURN,
            score_cutoff=STANDARD_SCORE_CUTOFF,
        )
        res_WR = process.extract(
            self.author_search_word,
            all_authors,
            scorer=fuzz.WRatio,
            limit=STANDARD_LENGTHS_TO_RETURN,
            score_cutoff=STANDARD_SCORE_CUTOFF,
        )

        # if no results
        if not res_r or not res_WR:
            return None, None

        if res_r[0][0] != res_WR[0][0]:
            # if WRatio and ratio return different top results, combine them
            authors_found = [res_r[0][0], res_WR[0][0]]
        else:
            # Otherwise, just keep one of them
            authors_found = [res_r[0][0]]

        authors_found.extend([r[0] for r in res_r])
        authors_found.extend([r[0] for r in res_WR])

        # remove duplicate author names
        seen = set()
        authors_found = [x for x in authors_found if not (x in seen or seen.add(x))]
        print("Authors found:", authors_found)
        return authors_found

    def _length_search(self):
        """
        return the length mentioned in the query
        """
        length_to_search_for = [le for le in ALL_LENGTHS if le.lower() in self.length_search_word.lower()]
        if length_to_search_for:
            return length_to_search_for[0]

    def _perform_special_token_sweep(self):
        """
        search for all the tokens mentioned in the query
        """
        if self.df_to_use is not None:
            df = self.df_to_use
        else:
            df = self.class_indices.df

        # author sweep
        author_search_word = [word for word in self.query_special_spl if AUTHOR_SEARCH_TOKEN in word]
        if author_search_word:
            self.author_search_word = author_search_word[0][2:]
            authors_found = self._author_search()
            if authors_found:
                self.au_tokens_filt = authors_found

        # length sweep
        length_search_word = [word for word in self.query_special_spl if LENGTH_SEARCH_TOKEN in word]

        if length_search_word:
            self.length_search_word = length_search_word[0][2:]
            length_found = self._length_search()
            if length_found:
                self.le_tokens_filt = length_found

    def _set_df_to_use(self):
        """
        set pair filtered dfs to use going while forward with the search
        """
        # if pair(s) is found
        if self.pairs_selected:
            print("Setting df to use.")
            self.df_to_use = self.class_indices.data[self.pairs_selected[0]]
            for pair in self.pairs_selected[1:]:
                self.df_to_use = self.df_to_use.append(self.class_indices.data[pair])
            # append the una rows of the first pair also
            self.df_to_use = self.df_to_use.append(
                self.class_indices.df.loc[
                    self.class_indices.df["story_id"].isin(self.class_indices.data_una[self.pairs_selected[0]])
                ]
            )
            print("Length of df to use: ", len(self.df_to_use.index.values))

    def _perform_pairing_sweep(self):
        """
        search for all the pairings mentioned in the query
        """
        # if nopair is specified, search only those.
        if "nopair" in self.query:
            res = ["NoPairs"]
            self.pairs_selected = res

        res = [pair for pair in PAIRS_TO_LOOK_FOR if pair.lower() in self.query.lower()]
        if res:
            # only two pairs (first two) will be considered, and one will be returned as such while
            # two will be returned like: if res is ['a', 'b'] then res to return will be res = ['a', 'b', 'a!b']
            if len(res) > 1:
                res = res[:2]
                other_pair = res[0] + "!" + res[1]
                res.append(other_pair)

            self.pairs_selected = res

            # remove pairs from query text
            l = [pair.lower() for pair in res]
            query = ""
            for word in self.query_spl:
                if word.lower() not in l:
                    query = query + " " + word
            # update query and its split and remove pairing names from them
            self.query = query.strip()
            self.query_spl = self.query.split(" ")
            print("Query after removing pairs: ", self.query)

        print("Pairs selected: ", self.pairs_selected)
        self._set_df_to_use()

    def _perform_phase_2_search(self):
        print("Performing phase 2 search now.")

        # default pairing index will be the Harmony index
        if self.df_to_use is None:
            self.psie_indices_filt = self.class_indices.psieindices["Harmony"]
        else:
            self.psie_indices_filt = self.class_indices.psieindices[self.pairs_selected[0]]

        ix = self.psie_indices_filt
        with ix.searcher() as searcher:
            or_group = qparser.OrGroup.factory(0.8)
            query = QueryParser("summary", ix.schema, group=or_group).parse(self.query)

            results = searcher.search(query)

            ids = []
            for hit in results:
                ids.append(int(hit["story_id"]))

            print("Phase 2 result ids: ", ids)

        # set result id to the story ids found
        if ids:
            self.result_ids = ids
            return self._return_res_ids(phase_one=False, query_to_search_empty=False)
        else:
            print("No indices found.")

    # def _get_embed_query(self):
    #     return self.st_model.encode([self.query])

    #     def _perform_phase_2_search(self):
    #         print('Performing phase 2 search now.')

    #         index = self.class_indices.sieindex
    #         _, indices = index.search(self._get_embed_query(), 5000)
    #         res_indices =  indices.tolist()[0]

    #         self.result_ids = [self.class_indices.sie_ids[i] for i in res_indices]
    # #         print('summ ids found:', self.result_ids)

    #         return self._return_res_ids(phase_one=False, query_to_search_empty=False)

    def _is_summ_token_present(self):
        summ_search_word = [word for word in self.query_spl if SUMM_TOKEN in word]
        if summ_search_word:
            for word in summ_search_word:
                word_sans_token = word[2:]
                self.query = self.query.replace(word, word_sans_token)
            print("Query after removing summary token: ", self.query)
            return True
        else:
            return False

    def _perform_phase_1_search(self):
        """
        Phase 1 of search---for title
        """
        self._perform_pairing_sweep()
        self._perform_special_token_sweep()
        print(f"Query is after pairing and tokens sweep: {self.query_spl}")

        if (
            self.query.strip() != ""
            and len(self.query_spl) > 0
            and len(self.query_spl) <= 7
            and not self._is_summ_token_present()
        ):
            print("Searching for title.")
            self.result_ids, self.dym_title = self._title_search()
            if self.result_ids:
                return self._return_res_ids(phase_one=True, query_to_search_empty=False)
            else:
                return self._perform_phase_2_search()
        elif len(self.query_spl) > 7 or self._is_summ_token_present():
            return self._perform_phase_2_search()
        else:
            print("No query left except special tokens.")
            if self.au_tokens_filt or self.le_tokens_filt:
                print("Only author or length token found.")
                return self._return_res_ids(phase_one=True, query_to_search_empty=True)
            else:
                # only pairings
                print("Only pairings found.")
                return self._return_res_ids(phase_one=True, query_to_search_empty=True)

    def _search_psie(self):
        return self._perform_phase_1_search()

    def search(self, query):
        self.query_special_spl = None
        self.query = None
        self.query_spl = None
        self.author_search_word = None
        self.length_search_word = None
        self.df_to_use = None
        self.au_tokens_filt = None
        self.le_tokens_filt = None
        self.pairs_selected = None
        self.st_model = None
        self.psie_indices_filt = None
        self.is_phase_2 = False

        self.result_ids = None
        self.dym_title = None

        self.query = query
        self._make_queries_and_load_model()
        return self._search_psie()

    def prepare_s_engine(self, override_for_hhr=False, pairs=None):
        if not override_for_hhr:
            indices = Indices()
        else:
            indices = Indices(pairs=pairs, override_for_hhr=override_for_hhr)

        indices.load_psieindices()
        self.class_indices = indices

    # MISC FUNCTIONS

    def get_story_link(self, story_id):
        return f"https://www.fanfiction.net/s/{story_id}"

    def get_story_link_ao3(self, story_id):
        return f"https://archiveofourown.org/works/{story_id}"

    def get_story_details(self, story_id):
        df = self.class_indices.df
        return df.loc[df.story_id == story_id]

    def get_all_harmony_ffn_fics(self):
        df = self.class_indices.df
        return df.loc[(df.Pairs == "Harmony") & (df.Medium == MEDIUM_FFN_COL_NAME)]

    def get_all_harmony_ao3_fics(self):
        df = self.class_indices.df
        return df.loc[(df.Pairs == "Harmony") & (df.Medium == MEDIUM_AO3_COL_NAME)]
