from django.urls import path, re_path

from . import views

urlpatterns = [
    # FFN/AO3 STORY LINKS
    path(
        "ffn/<str:story_id>/",
        views.GetStoryDetailsFfn.as_view(),
        name="get_storydetails_endpoint_ffn",
    ),
    path(
        "ao3/<str:story_id>/",
        views.GetStoryDetailsAo3.as_view(),
        name="get_storydetails_endpoint_ao3",
    ),
    # HHR STORY BLACKLIST PATHS
    path(
        "hhr_blacklist/",
        views.BlacklistView.as_view(),
        name="hhr_blacklist",
    ),
    path(
        "hhr_blacklist/new/<str:story_id>/",
        views.CreateOrAddBlacklistFic.as_view(),
        name="hhr_blacklist_add_or_modify",
    ),
    path(
        "au_ffn_profile/<str:au_id>",
        views.GetAuthorProfileDetailsFFN.as_view(),
        name="get_author_profile_ffn",
    ),
    path(
        "au_ao3_profile/<str:au_username>", views.GetAuthorProfileDetailsAo3.as_view(), name="get_author_profile_ao3"
    ),
]
