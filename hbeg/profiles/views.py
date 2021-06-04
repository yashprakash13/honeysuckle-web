from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from .models import *
from .forms import *
# import the searcher instance from core app
from core.views import instance
from core.searcher.constants import *

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
        else:
            # TODO: Handle errors
            pass



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
        stories = folder.story.all()
        context = {
            'form':FolderEditForm(instance=folder),
            'stories': stories
        }
        return render(request, 'profiles/folder_edit.html', context)
    
    def post(self, request, folder_id):
        folder = Folder.objects.filter(created_by=request.user).get(pk=folder_id)
        stories = folder.story.all()
        # 'form' for regualar folder properties edit
        form = FolderEditForm(request.POST, instance=folder)
        # 'form_story' for deleting stories in the folder
        form_story = FolderStoryEditForm(request.POST, stories_to_show=stories)
        
        # get stories selected to delete from folder
        stories_selected = request.POST.getlist('story_checkboxes')
        stories_selected = Story.objects.filter(pk__in=stories_selected)
        # delete selected stories from folder one by one
        for story in stories_selected:
            folder.story.remove(story)
        
        # save the regular form with title, description and visibility
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            print(form.cleaned_data)
            # TODO Handle the errors
        

    

class StoryDetailView(LoginRequiredMixin, View):
    """View Story detail and go to story/delete from folder options and 
        to add story rating alongwith.
    """
    def get(self, request, story_id):
        storygotten = instance.get_story_details(story_id)[COLS_TO_SHOW_STORY_DETAIL]
        story = storygotten.to_dict(orient='records')[0]
        story['link'] =  instance.get_story_link(story_id)
        context = {
            'story':story
        }

        return render(request, 'profiles/story_detail.html', context)


class StoryRateView(LoginRequiredMixin, View):
    """View to rate a story
    """
    def get(self, request, story_id):
        story_to_rate = instance.get_story_details(story_id)[COL_NAME_STORY]
        print(story_to_rate)
        context = {
            'storyname':story_to_rate[COL_NAME_STORY].values[0][0],
            'form': AddStoryRatingForm()
        }
        return render(request, 'profiles/story_rating.html', context)

    def post(self, request, story_id):
        # get the story name from story_id
        story_to_rate = instance.get_story_details(story_id)[COL_NAME_STORY]
        # display rating form
        form = FolderEditForm(request.POST)
        # get the rating choice selected
        choice = request.POST['rating']

        # check if user rating for this story exists
        exists_or_not = StoryRating.objects.filter(created_by = request.user, story_id=story_id)
        if exists_or_not:
            exists_or_not.update(rating=choice)
        else:
            StoryRating.objects.create(
                rating = choice,
                story_id = story_id,
                created_by = request.user
            )
        
        return redirect('profile')


class StoryAddView(LoginRequiredMixin, View):
    """View to add a story to folder(s)
    """
    def get(self, request, story_id):
        folders_of_user = Folder.objects.filter(created_by=request.user)
        context = {
            'folders':folders_of_user
        }
        return render(request, 'profiles/add_story_to_folder.html', context)
    
    def post(self, request, story_id):
        # get all folders from profile
        folders_of_user = Folder.objects.filter(created_by=request.user)
        # display form containing all folders
        form = AddStoryToFolderForm(request.POST, folders_to_show=folders_of_user)
        # get all folders selected to add the story into
        folders_selected = request.POST.getlist('folder_checkboxes')
        folders_selected = Folder.objects.filter(pk__in=folders_selected)
        # for every folder, create a story object if not already present and add it to folder(s)
        for folder in folders_selected:
            try:
                story = Story.objects.get(story_id=story_id)
                folder.story.add(Story.objects.get(story_id=story_id))
            except Story.DoesNotExist:
                storygotten = instance.get_story_details(story_id)[COLS_TO_SAVE_STORY]
                storygotten = storygotten.to_dict(orient='records')[0]
                storygotten['link'] = instance.get_story_link(story_id)
                story = Story(story_id=story_id, 
                              story_name=storygotten['title'], 
                              author_name=storygotten['author_name'],
                              link=storygotten['link'])
                story.save()

                folder.story.add(Story.objects.get(story_id=story_id))
                
        return redirect('search')

