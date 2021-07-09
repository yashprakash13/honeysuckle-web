from django.urls import include, path

# the Harmony section
urlpatterns = [path("", include("sections.harmony.urls"))]
