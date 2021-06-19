from django.urls import path
from . import views

urlpatterns = [
    path('', views.search, name='search'),
    path('about/', views.AboutView.as_view(), name="about"),
]
