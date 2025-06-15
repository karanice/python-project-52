from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from task_manager.users.forms import UserForm

class UserIndexView(View): # ДОБАВИТЬ ВЫВОД ОШИБОК
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        mssgs = messages.get_messages(request)
        return render(
            request,
            "users/index.html",
            context={ 'users': users,
                      'messages': mssgs,
            },
        )

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

class UserFormCreateView(View): # ТУТ НУЖНО УБРАТЬ ЧТЕНИЕ СООБЩЕНИЙ
    def get(self, request, *args, **kwargs):
        form = UserForm()
        mssgs = messages.get_messages(request)
        return render(request, "users/create.html", {"form": form, 'messages': mssgs})
    
    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Пользователь добавлен", 
                                 'alert alert-success alert-dismissible fade show')
            mssgs = messages.get_messages(request)
            return redirect(reverse('user_index'))
        mssgs = messages.get_messages(request)
        messages.add_message(request, messages.WARNING, "Проверьте заполняемые поля")
        return render(request, 'users/create.html', {'form': form, 'messages': mssgs})
    
class UserFormUpdateView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        user = User.objects.get(id=user_id)
        form = UserForm(instance=user)
        mssgs = messages.get_messages(request)
        return render(
            request, "users/update.html", {"form": form, "user_id": user_id}
        )
    
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        user = User.objects.get(id=user_id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Пользователь обновлён",
                                 'alert alert-success alert-dismissible fade show')
            return redirect(reverse("user_index"))

        return render(
            request, "users/update.html", {"form": form, "user_id": user_id}
        )
    
class UserFormDeleteView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        user = User.objects.get(id=user_id)
        mssgs = messages.get_messages(request)
        return render(
            request, "users/delete.html", {"user": user, "user_id": user_id}
        )
    
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        user = User.objects.get(id=user_id)
        if user:
            user.delete()
        messages.add_message(request, messages.SUCCESS, "Пользователь успешно удалён",
                             'alert alert-success alert-dismissible fade show')
        return redirect(reverse("user_index"))
