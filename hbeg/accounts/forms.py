from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Member
from hbeg.form_validators import *

class RegisterForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ('nickname', 'password1', 'password2')
    
    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if not check_password_size(password1):
            raise forms.ValidationError("The password is too short.")
    
    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        if not check_nickname_size(nickname):
            raise forms.ValidationError("The nickname is too short.")
        if not check_any_name_characters(nickname):
            raise forms.ValidationError("Sorry, the nickname can only have alphanumeric, _ or - characters.")
            