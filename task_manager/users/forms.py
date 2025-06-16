from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password1 = forms.CharField(
        label=("Пароль"),
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Пароль',
                   'class': 'form-control'}),
        help_text=("Ваш пароль должен содержать как минимум 3 символа."),
    )

    password2 = forms.CharField(
        label=("Подтверждение пароля"),
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Подтверждение пароля', 
                   'class': 'form-control'}),
        help_text=("Для подтверждения введите, пожалуйста, пароль ещё раз."),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 
                  'password1', 'password2')
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Имя пользователя',
        }
        help_texts = {
            'username': (
                '''Обязательное поле. Не более 150 символов. 
                Только буквы, цифры и символы @/./+/-/_.'''
            ),
        }
        widgets = {
            'username': forms.TextInput(
                attrs={'placeholder': 'Имя пользователя',
                       'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя',
                                                  'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия',
                                                 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        errors = []

        filtered = User.objects.filter(username=username)
        if self.instance.id:
            if filtered.exclude(id=self.instance.id).exists():
                self.add_error('username', 
                               'Пользователь с таким именем уже существует.')
        else:
            if filtered.exists():
                self.add_error('username', 
                               'Пользователь с таким именем уже существует.')

        if password1 and len(password1) < 3:
            errors.append('Введённый пароль слишком короткий. ' 
            'Он должен содержать как минимум 3 символа.')

        if password1 != password2:
            errors.append('Пароли не совпадают.')

        if errors:
            msg = " ".join(errors)
            self.fields['password2'].help_text = \
            f"{msg}Для подтверждения введите, пожалуйста, пароль ещё раз."
            for error in errors:
                self.add_error('password2', error)
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
