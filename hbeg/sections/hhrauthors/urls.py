from django.urls import include, path

from .views import *

urlpatterns = [
    path("authors/me", AuthorDashboardView.as_view(), name="author_dashboard"),
    path("authors/me/create_story", NewWorkView.as_view(), name="author_create_story"),
    path("authors/me/story/<str:workid>", WorkChaptersView.as_view(), name="author_story_chapters"),
]
