from django.shortcuts import render
from django.http import HttpResponse

from . import searcher

# prepare the search engine to receive queries
# instance = searcher.SearchEngine()
# instance.prepare_s_engine()

# the search view to receive queries and send results
def search(request):
    # get the search query from search bar
    # search_query = request.POST.get("query", " ")
    res_to_show = None
    # if search_query.strip() != "":
    #     # search the db here and get back resultant df
    #     res_df = instance.search(search_query)[['title', 'author_name', 'summary', 'rated', 'num_words']]
    #     # convert to list of dicts
    #     res_to_show = res_df.to_dict('records')

    return render(request, 'core/search.html'
    , {'results':[ {
        'title': 'Harry Potter and the Oroborus Light',
        'author_name':'Circusphoenix',
        'summary':'abc ighwo oihgowi oihoirwh hjiohji ohoih iihoarho;ioi owhiwriwij ohgihwariuohj ohwohiwohj iaihgiwrhiohiwrh ohairhw goww ghhaojg a hroahgw gw aajo jah  ha a jga',
        'rated':'T',
        'num_words':'297k',
        'status': 'Complete',
        'chars' : 'Harry P., Hermione G.',
        'genres':'Romance, Adventure'
    }]}
    )
