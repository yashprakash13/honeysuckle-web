from django.urls import path, include
from . import views

urlpatterns = [
    path('library/', views.AllStoriesView.as_view(), name="library"),
]
