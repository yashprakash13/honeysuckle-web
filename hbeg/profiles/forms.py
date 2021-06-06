from .models import *
from django import forms
from django.forms import ModelForm


class ProfileEditForm(ModelForm):
    """Form to edit a member profile
    """
    class Meta:
        model = Profile
        fields = ('bio', 'profile_pic', 'is_author')
        
    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['is_author'].widget.attrs['class'] = 'select'
        self.fields['bio'].widget.attrs['class'] = 'input'

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
        self.fields['folder_name'].widget.attrs['type'] = 'text'
        self.fields['folder_desc'].widget.attrs['class'] = 'input'
        self.fields['is_visible'].widget.attrs['class'] = 'select'



class FolderStoryEditForm(forms.Form):
    """ Form to delete stories from a folder
    """
    story_checkboxes = forms.MultipleChoiceField(
        widget = forms.CheckboxSelectMultiple,
    )
    def __init__(self, *args, **kwargs):
        story_list = kwargs.pop('stories_to_show', None)
        super(FolderStoryEditForm, self).__init__(*args, **kwargs)
        self.fields['story_checkboxes'] = forms.MultipleChoiceField(
                                                widget=forms.CheckboxSelectMultiple(), 
                                                choices=story_list)


class ContribStoryForm(ModelForm):
    """Form to Contribute new story to the database
    """
    class Meta:
        model = Story
        fields = ('link',)


class AddStoryToFolderForm(forms.Form):
    folder_checkboxes = forms.MultipleChoiceField(
        widget = forms.CheckboxSelectMultiple,
    )
    def __init__(self, *args, **kwargs):
        folder_list = kwargs.pop('folders_to_show', None)
        super(AddStoryToFolderForm, self).__init__(*args, **kwargs)
        self.fields['folder_checkboxes'] = forms.MultipleChoiceField(
                                                widget=forms.CheckboxSelectMultiple(), 
                                                choices=folder_list)
        

class AddStoryRatingForm(ModelForm):
    class Meta:
        model = StoryRating
        fields = ('rating', )

    def __init__(self, *args, **kwargs):
        super(AddStoryRatingForm, self).__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs['class'] = 'select'
