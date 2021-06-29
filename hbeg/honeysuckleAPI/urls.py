from django.urls import path, re_path
from . import views

urlpatterns = [
    path('ffn/<str:story_id>/', views.GetStoryDetailsFfn.as_view(), name="get_storydetails_endpoint_ffn"),
    path('ao3/<str:story_id>/', views.GetStoryDetailsAo3.as_view(), name="get_storydetails_endpoint_ao3"),
]


