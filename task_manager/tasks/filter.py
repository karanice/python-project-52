import django_filters
from django import forms
from django.contrib.auth.models import User

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

from .models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=('Статус'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label=('Исполнитель'),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields["executor"].label_from_instance = lambda obj: \
            f"{obj.first_name} {obj.last_name}"
        
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=('Метки'),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    user_tasks = django_filters.BooleanFilter(
        method='user_tasks_filter',
        label=('Только свои задачи'),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'user_tasks']       

    def user_tasks_filter(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset.all()