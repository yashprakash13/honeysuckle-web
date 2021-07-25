from django.urls import include, path

from .views import *

urlpatterns = [
    path("harmony/", CentralPageView.as_view(), name="harmony_central_page"),
    path("harmony/moments", MomentsView.as_view(), name="harmony_moments"),
    path("harmony/fthree", FabulousFicFeed.as_view(), name="harmony_f_three"),
    path("harmony/fics", FicsOptionsView.as_view(), name="harmony_fics_options"),
    path("harmony/fics/ffn", FicsViewFFN.as_view(), name="harmony_fics_ffn"),
    path("harmony/fics/ao3", FicsViewAO3.as_view(), name="harmony_fics_ao3"),
    path("harmony/authors", AuthorsView.as_view(), name="harmony_authors"),
]
