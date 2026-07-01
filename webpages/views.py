from django.shortcuts import render, redirect
from django.views import View


class Index_Page(View):
    def get(self, request):
        context = {}
        return render(request, 'home.html', context)