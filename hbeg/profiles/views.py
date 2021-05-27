from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from .models import *
from .forms import *


class ProfileView(LoginRequiredMixin, View):
    """View to display profile page
    """
    def get(self, request):
        profile = Profile.objects.filter(member = request.user)[0]
        folders = Folder.objects.filter(created_by = request.user)
        context = {
            'profile': profile,
            'folders':folders
        }

        return render(request, 'profiles/profile.html', context)


class ProfileSettingsView(LoginRequiredMixin, View):
    """View to edit profile
    """
    def get(self, request):
        return render(request, 'profiles/profile_settings.html', 
                    {'form':ProfileEditForm(initial={'is_author': request.user.profile.is_author})})
    
    def post(self, request):
        form = ProfileEditForm(request.POST, request.FILES, 
                                instance=request.user.profile, 
                                initial={'is_author': request.user.profile.is_author})
        if form.is_valid():
            if str(form.cleaned_data.get('bio')).strip() != '':
                choice = request.POST['is_author']
                print(choice)
                form.save()
            return redirect('profile')
        else:
            # TODO handle errors
            return redirect('profile')



class FolderDetailView(LoginRequiredMixin, View):
    """View to show detail view of a folder including stories within it
    """
    def get(self, request, folder_id):
        folder = Folder.objects.get(pk=folder_id)
        context = {
            'folder' : folder
        }

        return render(request, 'profiles/folder_detail.html', context)



class FolderAddView(LoginRequiredMixin, View):
    """View to add a new folder
    """
    def get(self, request):
        return render(request, 'profiles/folder_add.html', {'form': NewFolderForm()})

    def post(self, request):
        form = NewFolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.created_by = request.user
            folder.save()

            return redirect('profile')



class FolderDeleteView(LoginRequiredMixin, View):
    """View to delete a folder
    """
    def get(self, request, folder_id):
        folder = Folder.objects.filter(created_by = request.user).get(pk=folder_id)
        folder.delete()

        return redirect('profile')



class FolderEditView(LoginRequiredMixin, View):
    """View to edit a folder and its stories
    """
    def get(self, request, folder_id):
        folder = Folder.objects.filter(created_by=request.user).get(pk=folder_id)
        return render(request, 'profiles/folder_edit.html',
                    {'form':FolderEditForm(instance=folder)})
    
    def post(self, request, folder_id):
        folder = Folder.objects.filter(created_by=request.user).get(pk=folder_id)
        form = FolderEditForm(request.POST, instance=folder)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            print(form.cleaned_data)
            # TODO Handle the errors
        

    

class StoryDetailView(LoginRequiredMixin, View):
    """View Story detail and go to story/delete from folder options
    """
    def get(self, request, story_id):
        story = Story.objects.get(pk=story_id)
        context = {
            'story' : story
        }

        return render(request, 'profiles/story_detail.html', context)




