from django.urls import path
from . import views

urlpatterns = [
    path('me/', views.ProfileView.as_view(), name="profile"),
    path('folder/<int:folder_id>/', views.FolderDetailView.as_view(), name='folder_detail'),
    path('story/<int:story_id>/', views.StoryDetailView.as_view(), name='story_detail'),
    path('folder/new/', views.FolderAddView.as_view(), name='folder_add'),
    path('me/settings/', views.ProfileSettingsView.as_view(), name='profile_settings'),

]