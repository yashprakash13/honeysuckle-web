from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'profiles/profile.html')
