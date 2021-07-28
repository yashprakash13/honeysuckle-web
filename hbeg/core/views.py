from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from . import searcher
from .searcher.settings import *

# prepare the search engine to receive queries, this object will be used by other apps such as profiles too.
instance = searcher.SearchEngine()
if not DEBUGGING_WITHOUT_SEARCHER:
    instance.prepare_s_engine(pairs=HHR_SEARCHER_PAIR, override_for_hhr=OVERRIDE_FOR_HHR)

# the search view to receive queries and send results
def search(request):  # pragma: no cover
    # get the search query from search bar
    context = {}
    search_query = request.GET.get("query", " ")
    res_to_show = None
    if search_query.strip() != "":
        # search the db here and get back resultant df
        print("Inside search GET block.")
        res_df = instance.search(search_query)
        if res_df is not None:
            res_df = res_df[searcher.constants.COLS_TO_SHOW_STORY_DETAIL]
            # convert to list of dicts
            res_to_show = res_df.to_dict("records")
            context["results"] = res_to_show
        else:
            context["nores"] = True
            # context["nores"] = range(1, 17)
        context["query"] = search_query

    context["page_title"] = "HisBrownEyedGirl"

    return render(
        request,
        "core/search.html",
        context
        # , {'results':[ {
        #     'story_id': 2963991,
        #     'title': 'Harry Potter and the Oroborus Light',
        #     'author_name':'Circusphoenix',
        #     'summary':'abc ighwo oihgowi oihoirwh hjiohji ohoih iihoarho;ioi owhiwriwij ohgihwariuohj ohwohiwohj iaihgiwrhiohiwrh ohairhw goww ghhaojg a hroahgw gw aajo jah  ha a jga',
        #     'rated':'T',
        #     'num_words':'297k',
        #     'status': 'Complete',
        #     'chars' : 'Harry P., Hermione G.',
        #     'genres':'Romance, Adventure'
        # }]}
    )


class AboutView(View):
    """View to show About HBEG page"""

    def get(self, request):
        context = {"page_title": "About HBEG"}
        return render(request, "core/about.html", context=context)


class HoneysuckleDashBoard(View):
    """Honeysuckle discord bot dashboard"""

    def get(self, request):
        return render(request, "core/honeysuckle_dashboard.html")
