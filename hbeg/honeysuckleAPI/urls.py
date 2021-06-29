from django.urls import path, re_path
from . import views

urlpatterns = [
    path('ffn/<str:story_id>/', views.GetStoryDetailsFfn.as_view(), name="get_storydetails_endpoint"),
]


