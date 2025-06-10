# from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib import messages


class IndexView(View):
    
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "base.html",
            context={
            },
        )
    
class UserIndexView(View):
    template_name = "index.html"
    
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "users/index.html",
            context={
            },
        )