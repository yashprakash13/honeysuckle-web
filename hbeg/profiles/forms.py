from .models import *
from django.forms import ModelForm


class NewFolderForm(ModelForm):
    """Form to create a new folder
    """
    class Meta:
        model = Folder
        fields = ('folder_name', 'folder_desc', 'is_visible')

class ContribStoryForm(ModelForm):
    """Form to Contribute new story to the database
    """
    class Meta:
        model = Story
        fields = ('story_name', 'author_name', 'link')


class ProfileEditForm(ModelForm):
    """Form to edit a member profile
    """
    class Meta:
        model = Profile
        # TODO: Add another field to change nickname too
        fields = ('bio', 'is_author')
