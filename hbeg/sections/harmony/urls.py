from django.urls import include, path

from .views import *

urlpatterns = [
    path("harmony/", CentralPageView.as_view(), name="harmony_central_page"),
    path("harmony/moments", MomentsView.as_view(), name="harmony_moments"),
    path("harmony/fthree", FabulousFicFeed.as_view(), name="harmony_f_three"),
    # author reg
    path("harmony/author_reg", AuthorRegView.as_view(), name="author_reg"),
]
