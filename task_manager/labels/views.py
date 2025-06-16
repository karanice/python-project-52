from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label


class IndexView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'


class LabelCreateFormView(LoginRequiredMixin, CreateView):
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('label_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = False
        return context
    
    def form_valid(self, form):
        messages.success(self.request, ("Метка успешно создана"),
                         'alert alert-success alert-dismissible fade show')
        return super().form_valid(form)
    

class LabelUpdateFormView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('label_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context
    
    def form_valid(self, form):
        messages.success(self.request, ("Метка успешно изменена"),
                         'alert alert-success alert-dismissible fade show')
        return super().form_valid(form)
    

class LabelDeleteFormView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('label_index')
    context_object_name = 'label'

    def form_valid(self, form):
        label = self.get_object()
        if label.task_set.exists():
            messages.error(self.request, 
                           ('Невозможно удалить метку, потому что она используется'),
                           'alert alert-danger alert-dismissible fade show')
            return redirect(self.success_url)
        messages.success(self.request, ('Метка успешно удалена'),
                         'alert alert-success alert-dismissible fade show')
        return super().form_valid(form)
