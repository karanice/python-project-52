from django import forms

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

from .models import Task


class TaskForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].queryset = Status.objects.all()
        self.fields['executor'].label_from_instance = (
            lambda obj: f"{obj.first_name} {obj.last_name}"
        )
        self.fields['labels'].queryset = Label.objects.all()

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels',]

        labels = {
            'name': ('Имя'),
            'description': ('Описание'),
            'status': ('Статус'),
            'executor': ('Исполнитель'),
            'labels': ('Метки'),
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': ('Имя'),
                'class': 'form-control',
                'required': False,
            }),
            'description': forms.Textarea(attrs={
                'placeholder': ('Описание'),
                'class': 'form-control',
                'required': False,
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
            }),
            'executor': forms.Select(attrs={
                'class': 'form-control',
                'required': False,
            }),
            'labels': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': '4',
            }),
        }