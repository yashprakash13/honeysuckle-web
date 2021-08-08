from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from .forms import *
from .models import *


class AuthorDashboardView(LoginRequiredMixin, View):
    """the author dashboard view"""

    def get(self, request):
        context = {}
        # all works by the user
        works = Works.objects.filter(author=request.user)

        if len(works) == 0:
            context["no_works"] = True
            context["no_reviews"] = True
            context["no_drafts"] = True
        elif len(works) > 0:
            # all reviews for user
            reviews = Reviews.objects.filter(work__in=works)
            if len(reviews) == 0:
                context["no_reviews"] = True

            # all drafts by the user
            drafts = Chapters.objects.filter(work__in=works, is_published=False)
            if len(drafts) == 0:
                context["no_drafts"] = True

            # compile a few works to display in the dashboard
            for work in works[:4]:
                work_chapters = Chapters.objects.filter(work=work)
                work.chapters = len(work_chapters)
                words = 0
                for chapter in work_chapters:
                    words += chapter.words
                work.words = words

            context["works"] = works[:4]

        return render(request, "hhrauthors/author_dashboard.html", context=context)


class NewWorkView(LoginRequiredMixin, View):
    """view to add a new work/story"""

    def get(self, request):
        context = {"form": NewWorkForm()}

        return render(request, "hhrauthors/new_story.html", context=context)

    def post(self, request):
        form = NewWorkForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()

            return redirect("author_story_chapters", workid=story.id)

        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, f"{item}")
            return render(request, "hhrauthors/new_story.html", {"form": form})


class WorkChaptersView(LoginRequiredMixin, View):
    """view to show/add/modify chapters of a story"""

    def get(self, request, workid):
        context = {}
        return render(request, "hhrauthors/story_chapters.html", context=context)
