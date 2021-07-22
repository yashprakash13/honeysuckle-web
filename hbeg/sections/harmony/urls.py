from django.urls import include, path

from .views import *

urlpatterns = [
    path("harmony/", CentralPageView.as_view(), name="harmony_central_page"),
    path("harmony/moments", MomentsView.as_view(), name="harmony_moments"),
]
