from django.urls import include, path

from .views import *

urlpatterns = [
    path("authors/me", AuthorDashboardView.as_view(), name="author_dashboard"),
]
