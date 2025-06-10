from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib import messages

# Create your views here.

class UserIndexView(View): # возможно, лучше будет переназвать без User?
    
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "users/index.html",
            context={
            },
        )
