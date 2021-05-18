from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from .forms import RegisterForm


def login(request):
    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print('Yes form is valid.')
            member = form.save()
            raw_password = form.cleaned_data.get('password1')
            # member = authenticate(request, nickname=member.nickname, password=raw_password)
            # if member is not None:
            #     # login(request, member)
            #     print('Logged in with: ', member.nickname)
            return redirect('search') # TODO should go to profile here
        else:
            print('Some error happend.')
            
    else:
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})
    
