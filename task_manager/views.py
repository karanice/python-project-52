from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(
            request,
            "base.html",
            context={
            },
        )
    

class UserLogInFormView(View):

    def get(self, request, *args, **kwargs):
        mssgs = messages.get_messages(request)
        return render(
            request, 
            "registration/login.html",
            {'messages': mssgs}
        )

    def post(self, request, *args, **kwargs):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, "Вы залогинены", 
                                 'alert alert-success ' 
                                 'alert-dismissible fade show')
            return redirect(reverse("main"))
        else:
            return render(request, "registration/login.html", {"no_user": True})


class UserLogOutFormView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.INFO, "Вы разлогинены", 
                                 'alert alert-info alert-dismissible fade show')
        return redirect(reverse("main"))

