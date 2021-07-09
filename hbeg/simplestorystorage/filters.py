import django_filters

from profiles.models import Story


class AllStoriesFilter(django_filters.FilterSet):
    class Meta:
        model = Story
        fields = {
            "story_name": ["icontains"],
            "author_name": ["icontains"],
        }
