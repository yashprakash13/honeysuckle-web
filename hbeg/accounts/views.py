from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
# import custom Register form
from .forms import RegisterForm

class RegisterView(View):
    """View to register a user
    """
    def get(self, request):
        return render(request, 'accounts/register.html', {'form': RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            member = form.save()
            nickname, password = form.cleaned_data.get('nickname'), form.cleaned_data.get('password1')
            member = authenticate(nickname=nickname, password=password)
            login(self.request, member)
            # go to profile page upon redirect
            return redirect('profile')
        else:
            # check for registration errors
            password1 = form.data['password1']
            password2 = form.data['password2']
            nickname = form.data['nickname']
            for msg in form.errors.as_data():
                if msg == 'nickname':
                    messages.error(request, f"Chosen nickname cannot be used as a valid nickname.")
                if msg == 'password2' and password1 == password2:
                    messages.error(request, f"Selected password: is not strong enough.")
                elif msg == 'password2' and password1 != password2:
                    messages.error(request, f"The Passwords do not match.")
            return render(request, 'accounts/register.html', {'form': RegisterForm()})
