from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from task_manager.users.forms import UserForm


class CustomLoginRequiredMixin(LoginRequiredMixin):  
    def dispatch(self, request, *args, **kwargs):  
        if not request.user.is_authenticated:
            messages.add_message(request, messages.WARNING, 
                                 "Вы не авторизованы! " 
                                 "Пожалуйста, выполните вход.", 
                                 'alert alert-danger ' 
                                 'alert-dismissible fade show')
            return redirect(reverse('login'))  
        return super().dispatch(request, *args, **kwargs)  
    

class UserIndexView(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        mssgs = messages.get_messages(request)
        return render(
            request,
            "users/index.html",
            context={'users': users,
                      'messages': mssgs,
            },
        )


class UserFormCreateView(View):
    def get(self, request, *args, **kwargs):
        form = UserForm()
        mssgs = messages.get_messages(request)
        return render(request, "users/create.html", 
                      {"form": form, 'messages': mssgs})
    
    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 
                                 "Пользователь успешно зарегистрирован", 
                                 'alert alert-success ' 
                                 'alert-dismissible fade show')
            return redirect(reverse('login'))
        return render(request, 'users/create.html', {'form': form})
    

class UserFormUpdateView(CustomLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        user = User.objects.get(id=user_id)

        if request.user != user:
            messages.add_message(request, messages.WARNING, 
                                 "У вас нет прав для изменения " 
                                 "другого пользователя.", 
                                 'alert alert-danger ' 
                                 'alert-dismissible fade show')
            return redirect(reverse('user_index'))
            
        form = UserForm(instance=user)
        return render(
            request, "users/update.html", {"form": form, "user_id": user_id}
        )
    
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        user = User.objects.get(id=user_id)

        if request.user != user:
            messages.add_message(request, messages.WARNING, 
                                 "У вас нет прав для изменения " 
                                 "другого пользователя.", 
                                 'alert alert-danger ' 
                                 'alert-dismissible fade show')
            return redirect(reverse('user_index'))
        
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 
                                 "Пользователь успешно изменен",
                                 'alert alert-success ' 
                                 'alert-dismissible fade show')
            return redirect(reverse("user_index"))

        return render(
            request, "users/update.html", {"form": form, "user_id": user_id}
        )
    

class UserFormDeleteView(CustomLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        user = User.objects.get(id=user_id)

        if request.user != user:
            messages.add_message(request, messages.WARNING, 
                                 "У вас нет прав для изменения " 
                                 "другого пользователя.", 
                                 'alert alert-danger ' 
                                 'alert-dismissible fade show')
            return redirect(reverse('user_index'))
        
        return render(
            request, "users/delete.html", {"user": user, "user_id": user_id}
        )
    
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        user = User.objects.get(id=user_id)
        
        if request.user != user and not request.user.is_superuser:
            messages.add_message(request, messages.WARNING, 
                                 "У вас нет прав для изменения " 
                                 "другого пользователя.", 
                                 'alert alert-danger ' 
                                 'alert-dismissible fade show')
            return redirect(reverse('user_index'))

        if user.tasks_created.exists():
            messages.add_message(self.request, messages.ERROR,
                            ('''Невозможно удалить пользователя, 
                            потому что он используется'''),
                            'alert alert-danger ' 
                            'alert-dismissible fade show')
            return redirect(reverse("user_index"))
    
        user.delete()
        messages.add_message(request, messages.SUCCESS, 
                             "Пользователь успешно удален",
                             'alert alert-success ' 
                             'alert-dismissible fade show')
        return redirect(reverse("user_index"))
