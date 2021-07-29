from threading import Thread

from core.searcher.settings import DEBUGGING_WITHOUT_SEARCHER
from django.shortcuts import render
from django.views import View

from .dailyfeed.constants import HP_BOOK_CHOICES
from .dailyfeed.feedmaker import FeedMaker
from .fabfics.fabfics import HHrFicLoader
from .models import *

# load fics+authors
if not DEBUGGING_WITHOUT_SEARCHER:
    hhr_fic_loader = HHrFicLoader()


class CentralPageView(View):
    """View to display the main HHr page"""

    def get(self, request):
        context = {}
        return render(request, "harmony/main_view.html", context=context)


class FabulousFicFeed(View):
    """View to display the HHr fic feed from other ff websites"""

    def get(self, request):
        feed = FeedMaker()
        feed = feed.get_feed()
        context = {"works": feed}
        return render(request, "harmony/f_three.html", context=context)


class MomentsView(View):
    """View for appreciating HHr moments in canon"""

    def get(self, request):
        books = [pair[1] for pair in HP_BOOK_CHOICES]
        all_moments = {}
        for book, choice in zip(books, HP_BOOK_CHOICES):
            all_moments[book] = HarmonyMomentsModel.objects.filter(book__in=(choice)).values_list("moment", flat=True)
        context = {"bookwise_moments": all_moments}

        return render(request, "harmony/moments.html", context=context)


class FicsOptionsView(View):
    """View to show different website options for HHr fics"""

    def get(self, request):
        return render(request, "harmony/fics_options_view.html")


class FicsViewFFN(View):
    """View to show all HHr fics from FFN"""

    def get(self, request):
        context = {}
        context["all_fics"] = hhr_fic_loader.ffn_fics
        context["website"] = "FFN"
        return render(request, "harmony/fics_view.html", context=context)


class FicsViewAO3(View):
    """View to show all HHr fics from AO3"""

    def get(self, request):
        context = {}
        context["all_fics"] = hhr_fic_loader.ao3_fics
        context["website"] = "AO3"
        return render(request, "harmony/fics_view.html", context=context)


class AuthorsView(View):
    """View to show all HHr Authors"""

    def get(self, request):
        context = {"all_authors_ffn": hhr_fic_loader.authors_ffn, "all_authors_ao3": hhr_fic_loader.authors_ao3}
        return render(request, "harmony/authors_view.html", context=context)
