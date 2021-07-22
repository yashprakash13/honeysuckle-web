from threading import Thread

from django.shortcuts import render
from django.views import View

from .dailyfeed.constants import HP_BOOK_CHOICES
from .dailyfeed.feedmaker import FeedMaker
from .models import *


class CentralPageView(View):
    def get(self, request):
        feed = FeedMaker()
        feed = feed.get_feed()
        context = {"works": feed}
        return render(request, "harmony/main_view.html", context=context)


class MomentsView(View):
    def get(self, request):
        books = [pair[1] for pair in HP_BOOK_CHOICES]
        all_moments = {}
        for book, choice in zip(books, HP_BOOK_CHOICES):
            all_moments[book] = HarmonyMomentsModel.objects.filter(book__in=(choice)).values_list("moment", flat=True)
        context = {"bookwise_moments": all_moments}

        return render(request, "harmony/moments.html", context=context)
