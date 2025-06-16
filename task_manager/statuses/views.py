from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class IndexView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'


class StatusCreateFormView(LoginRequiredMixin, CreateView):
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('status_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = False
        return context
    
    def form_valid(self, form):
        messages.success(self.request, ("Статус успешно создан"),
                         'alert alert-success alert-dismissible fade show')
        return super().form_valid(form)
    

class StatusUpdateFormView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('status_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context
    
    def form_valid(self, form):
        messages.success(self.request, ("Статус успешно изменен"),
                         'alert alert-success alert-dismissible fade show')
        return super().form_valid(form)
    

class StatusDeleteFormView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('status_index')
    context_object_name = 'status'

    def form_valid(self, form):
        status = self.get_object()
        if status.task_set.exists():
            messages.error(self.request, 
                           ('''Невозможно удалить статус, 
                           потому что он используется'''),
                           'alert alert-danger alert-dismissible fade show')
            return redirect(self.success_url)
        messages.success(self.request, ('Статус успешно удален'),
                         'alert alert-success alert-dismissible fade show')
        return super().form_valid(form)
