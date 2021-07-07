from django.urls import path, re_path

from . import views


urlpatterns = [
    # path("signup/", views.signup, name="account_signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
]
