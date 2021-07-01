from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from profiles.models import StoryRating, Story
from core.views import instance
from core.searcher.constants import *

from .filters import AllStoriesFilter

RATING_MAPPING = {
    'O' : 5,
    'E' : 4,
    'A' : 3,
    'P' : 2,
    'D' : 1,
    'T' : 0
}
def get_rating(char_rating):
    return RATING_MAPPING[char_rating]



class AllStoriesView(LoginRequiredMixin, View):
    """View to display all stories page
    """
    
    def get(self, request):
        # quereyset of tuple --> ('story_id', 'rating')
        all_stories_queryset = StoryRating.objects.filter(created_by=request.user).values_list('story_id', 'rating')
        # list of above quereyset
        id_rating_list = list(all_stories_queryset)
        # dict of above quereyset
        id_rating_dict = dict((storyid, rating) for storyid, rating in id_rating_list)
        # list of story_ids from above queryset
        idlist = [obj[0] for obj in id_rating_list]

        # get corresponding stories from id list
        story_filter = AllStoriesFilter(request.GET, queryset=Story.objects.filter(story_id__in=idlist))
        all_stories = story_filter.qs.values()
        # all_stories = Story.objects.filter(story_id__in=idlist).values()
        # create (story, rating) tuple for all stories to display 
        all_stories = [(story, id_rating_dict[story['story_id']]) for story in all_stories]

        context = {
            'stories' : all_stories,
            'filter': story_filter,
        }
        return render(request, 'simplestorystorage/all_stories.html', context)
