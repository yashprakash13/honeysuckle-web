from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from .forms import *
from profiles.models import Folder, Profile, ProfileBadges
from accounts.models import Member

# import the searcher instance from core app
from core.views import instance
from core.searcher.constants import *
from core.searcher import utils

class PublicProfileView(View):
    """View to show public profile view of any given nickname from the URL
    """
    def get(self, request, nickname):
        nickname = nickname[1:] #remove @ symbol
        member = Member.objects.filter(nickname=nickname).first()
        if not member:
            context_error = {
                'nickname':nickname
            }
            return render(request, 'public/error_404.html', context_error)
        profile = Profile.objects.filter(member = member).first()
        folders = Folder.objects.filter(created_by = member, is_visible=True)
        p_badges = ProfileBadges.objects.filter(badges_for=member)[0]
        context = {
            'profile':profile,
            'folders':folders,
            'badges' : p_badges
        }
        return render(request, 'public/public_profile.html', context)


class PublicProfileFolderDetail(View):
    """View to show public profile folder detail view 
    """
    def get(self, request, folder_id):
        folder = Folder.objects.get(pk=folder_id)
        context = {
            'folder':folder
        }
        return render(request, 'public/public_folder_detail.html', context)


class PublicProfileStoryDetailView(View):
    """View to show public profile story detail view 
    """
    def get(self, request, story_id):
        storygotten = instance.get_story_details(story_id)[COLS_TO_SHOW_STORY_DETAIL]
        story = storygotten.to_dict(orient='records')[0]
        story['link'] =  instance.get_story_link(story_id)
        story['genres'] = utils.get_clean_genres(story['genres'])
        story['characters'] = story['characters'][1:-1]
        context = {
            'story':story
        }

        return render(request, 'public/public_story_detail.html', context)

