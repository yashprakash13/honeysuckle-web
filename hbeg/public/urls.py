from django.urls import path, re_path
from . import views

urlpatterns = [
    path("<nickname>/", views.PublicProfileView.as_view(), name="public_profile"),
    path(
        "folder/<int:folder_id>/",
        views.PublicProfileFolderDetail.as_view(),
        name="public_folder_detail",
    ),
    path(
        "story/<int:story_id>/",
        views.PublicProfileStoryDetailView.as_view(),
        name="public_story_detail",
    ),
]
