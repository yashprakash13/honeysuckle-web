from .models import *
from django import forms
from django.forms import ModelForm


class ProfileEditForm(ModelForm):
    """Form to edit a member profile
    """
    class Meta:
        model = Profile
        fields = ('bio', 'profile_pic', 'is_author')
        widgets = {
          'is_author': forms.Select(attrs={'class': 'select'}),
        }
    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)



class NewFolderForm(ModelForm):
    """Form to create a new folder
    """
    # TODO: Make folder desc optional
    class Meta:
        model = Folder
        fields = ('folder_name', 'folder_desc', 'is_visible')



class FolderEditForm(ModelForm):
    """Form to edit a folder
    """
    class Meta:
        model = Folder
        fields = ('folder_name', 'folder_desc', 'is_visible')

    def __init__(self, *args, **kwargs):
        super(FolderEditForm, self).__init__(*args, **kwargs)
        self.fields['folder_name'].widget.attrs['class'] = 'input'
        self.fields['folder_name'].widget.attrs['v-model'] = 'subtitle'
        self.fields['folder_desc'].widget.attrs['class'] = 'textarea'
        self.fields['is_visible'].widget.attrs['class'] = 'select'

class ContribStoryForm(ModelForm):
    """Form to Contribute new story to the database
    """
    class Meta:
        model = Story
        fields = ('link',)
