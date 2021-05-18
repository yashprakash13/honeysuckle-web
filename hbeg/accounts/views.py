from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
# import custom Register form
from .forms import RegisterForm

# def register(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             member = form.save()
#             raw_password = form.cleaned_data.get('password1')
#             # member = authenticate(request, nickname=member.nickname, password=raw_password)
#             # if member is not None:
#             #     # login(request, member)
#             #     print('Logged in with: ', member.nickname)
#             return redirect('search') # TODO should go to profile here
        
#     else:
#         form = RegisterForm()
#         return render(request, 'accounts/register.html', {'form': form})

class RegisterView(View):
    def get(self, request):
        return render(request, 'accounts/register.html', {'form': RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            member = form.save()
            nickname, password = form.cleaned_data.get('nickname'), form.cleaned_data.get('password1')
            member = authenticate(nickname=nickname, password=password)
            login(self.request, member)
            return redirect('profile')



class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts/profile.html')
