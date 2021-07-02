from django.db import models
from accounts.models import Member
import os
from ckeditor.fields import RichTextField
from django.conf import settings

# define a single story
class Story(models.Model):
    story_id = models.CharField(max_length=30)
    story_name = models.CharField(max_length=100)
    author_name = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-added_on']
        verbose_name_plural = 'Stories'

    def __str__(self):
        return self.story_name



# to define the story rating
class StoryRating(models.Model):
    RATING_CHOICES = (
        ('O', 'Outstanding'),
        ('E', 'Exceeds Expectations'),
        ('A', 'Acceptable'),
        ('P', 'Poor'),
        ('D', 'Dreadful'),
        ('T', 'Troll')
    )
    rating = models.CharField(max_length=50, choices=RATING_CHOICES, null=True, blank=True)
    story_id = models.CharField(max_length=30)
    created_by = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='StoryRating')

    def __str__(self):
        return f"{self.story_id}_rating_by_{self.created_by.nickname}"
    


# to contribute a new story
class StoryContrib(models.Model):
    link = models.CharField(max_length=100)
    given_by = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='StoryContrib')
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.is_accepted}_with_{self.link}_by_{self.given_by.nickname}"
    


# to define a folder to keep stories
class Folder(models.Model):
    folder_name = models.CharField(max_length=120)
    folder_desc = models.TextField(blank=True, null=True)
    BOOL_VISIBILITY_CHOICES = ((True, 'Visible'), (False, 'Invisible'))
    is_visible = models.BooleanField(choices=BOOL_VISIBILITY_CHOICES, default=True)
    created_by = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='Folders')
    created_at = models.DateTimeField(auto_now_add=True)
    story = models.ManyToManyField(Story, null=True, blank=True)

    def __str__(self):
        return self.folder_name
    
    class Meta:
        verbose_name_plural = 'Folders'
        ordering = ['-created_at']


    
# Define the profile created upon member registration
class Profile(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    bio = RichTextField(null=True, blank=True)
    BOOL_ISAUTHOR_CHOICES = ((True, 'Yes,I am.'), (False, 'Nope.'))
    is_author = models.BooleanField(choices=BOOL_ISAUTHOR_CHOICES, default=False)
    ffn_url = models.CharField(max_length=100, null=True, blank=True)
    story_contribs = models.PositiveIntegerField(default=0)
    story_referrals = models.PositiveIntegerField(default=0)
    is_early_adopter = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.member.nickname)
