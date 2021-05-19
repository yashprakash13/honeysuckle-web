from django.urls import path
from . import views

urlpatterns = [
    path('me/', views.ProfileView.as_view(), name="profile"),
]