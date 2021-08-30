from threading import Thread

from core.searcher.settings import DEBUGGING_WITHOUT_SEARCHER
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from .dailyfeed.constants import HP_BOOK_CHOICES
from .dailyfeed.feedmaker import FeedMaker
from .models import *


class CentralPageView(View):
    """View to display the main HHr page"""

    def get(self, request):
        context = {}
        if HarmonyAuthorReg.objects.filter(member=request.user).exists():
            context["author_reg_visible"] = False
        else:
            context["author_reg_visible"] = True
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


class AuthorRegView(LoginRequiredMixin, View):
    """View to sign up authors"""

    def get(self, request):
        return render(request, "harmony/author_registration_page.html")

    def post(self, request):
        context = {}
        # store author request if not already present from the author
        if request.POST.get("author_reg_btn") and not HarmonyAuthorReg.objects.filter(member=request.user).exists():
            HarmonyAuthorReg.objects.create(member=request.user)
            context["reg_done"] = True
        return render(request, "harmony/author_registration_page.html", context=context)
