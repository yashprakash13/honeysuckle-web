from ckeditor.widgets import CKEditorWidget
from django import forms
from django.forms import ModelForm

from .models import *


class NewWorkForm(ModelForm):
    """Form to add a new story"""

    class Meta:
        model = Works
        fields = ("title", "description", "rating", "genres", "status")

    def __init__(self, *args, **kwargs):
        super(NewWorkForm, self).__init__(*args, **kwargs)
        self.fields["title"].widget.attrs["class"] = "input"
        self.fields["description"].widget.attrs["class"] = "textarea"
        self.fields["description"].widget.attrs["maxlength"] = "999"
        self.fields["rating"].widget.attrs["class"] = "select"
        self.fields["rating"].widget.attrs["id"] = "select-options-new-work"
        self.fields["genres"].widget.attrs["class"] = "select"
        self.fields["genres"].widget.attrs["id"] = "select-options-new-work"
        self.fields["status"].widget.attrs["class"] = "select"
        self.fields["status"].widget.attrs["id"] = "select-options-new-work"

        self.fields["title"].error_messages["required"] = "Story title is required."
        self.fields["description"].error_messages["required"] = "Story description is required."
        self.fields["rating"].error_messages["required"] = "Story rating is required."
        self.fields["genres"].error_messages["required"] = "Story genres is required."
        self.fields["status"].error_messages["required"] = "Story status is required."
