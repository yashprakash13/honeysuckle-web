from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from .models import *


class AuthorDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        context = {}
        # all works by the user
        works = Works.objects.filter(author=request.user, is_published=True)
        if len(works) == 0:
            context["no_works"] = True
            context["no_reviews"] = True

        # all reviews for user
        if len(works) > 0:
            reviews = Reviews.objects.filter(work__in=works)
            if len(reviews) == 0:
                context["no_reviews"] = True

        # all drafts by the user
        drafts = Works.objects.filter(author=request.user, is_published=False)
        if len(drafts) == 0:
            context["no_drafts"] = True

        return render(request, "hhrauthors/author_dashboard.html", context=context)
