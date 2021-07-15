from django.shortcuts import render
from django.views import View


class CentralPageView(View):
    def get(self, request):
        return render(request, "harmony/main_view.html")
