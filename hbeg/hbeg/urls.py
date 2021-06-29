from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('itisme/', admin.site.urls),
    path('', include('core.urls')),
    path('acc/', include('accounts.urls')),
    path('profiles/', include('profiles.urls')),
    path('hbeg/', include('public.urls')), 
    path('profiles/', include('simplestorystorage.urls')), 

    # Honeysuckle API
    path('hsapi/', include('honeysuckleAPI.urls')), 
]
urlpatterns +=  static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

