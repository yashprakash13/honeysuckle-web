from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(Folder)
admin.site.register(Story)
admin.site.register(Tag)
admin.site.register(StoryRating)
admin.site.register(StoryContrib)
admin.site.register(ProfileBadges)


