from threading import Thread

from django.shortcuts import render
from django.views import View

from .dailyfeed.feedmaker import FeedMaker


class CentralPageView(View):
    def get(self, request):
        feed = FeedMaker()
        feed = feed.get_feed()
        context = {"works": feed}
        return render(request, "harmony/main_view.html", context=context)
