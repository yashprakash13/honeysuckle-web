from django.urls import path
from . import views

urlpatterns = [
    path('me/', views.ProfileView.as_view(), name="profile"),
    path('me/settings/', views.ProfileSettingsView.as_view(), name='profile_settings'),
    path('folder/<int:folder_id>/', views.FolderDetailView.as_view(), name='folder_detail'),
    path('folder/new/', views.FolderAddView.as_view(), name='folder_add'),
    path('folder/<int:folder_id>/edit/', views.FolderEditView.as_view(), name='folder_edit'),
    path('folder/<int:folder_id>/delete/', views.FolderDeleteView.as_view(), name='folder_delete'),
    path('story/<int:story_id>/', views.StoryDetailView.as_view(), name='story_detail'),
    path('story/<int:story_id>/add/', views.StoryAddView.as_view(), name='story_add'),
    path('story/<int:story_id>/ratestory/', views.StoryRateView.as_view(), name='story_rating'),
    path('contrib/', views.StoryContribView.as_view(), name='story_contrib'),

]