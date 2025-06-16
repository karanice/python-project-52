from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task

from .filter import TaskFilter


class IndexView(LoginRequiredMixin, FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'


class TaskCreateFormView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('task_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = False
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, ("Задача успешно создана"),
                         'alert alert-success alert-dismissible fade show')
        return super().form_valid(form)
    

class TaskUpdateFormView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('task_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, ("Задача успешно изменена"),
                         'alert alert-success alert-dismissible fade show')
        return super().form_valid(form)
    

class TaskDeleteFormView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('task_index')
        
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        if task.author != request.user and not request.user.is_superuser:
            messages.error(request, 
                           ('Задачу может удалить только ее автор'),
                           'alert alert-danger alert-dismissible fade show')
            return redirect('task_index')
        task.delete()
        messages.success(self.request, ('Задача успешно удалена'),
                         'alert alert-success alert-dismissible fade show')
        return redirect('task_index')

    def get_object(self, queryset=None):
        return get_object_or_404(Task, pk=self.kwargs['pk'])
    

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'