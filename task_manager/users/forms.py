from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(
        label=("Пароль"),
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'form-control'}),
        help_text=("Ваш пароль должен содержать как минимум 3 символа."),
    )

    confirm_password = forms.CharField(
        label=("Подтверждение пароля"),
        widget=forms.PasswordInput(attrs={'placeholder': 'Подтверждение пароля', 'class': 'form-control'}),
        help_text=("Для подтверждения введите, пожалуйста, пароль ещё раз."),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'confirm_password')
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
            'username': forms.TextInput(attrs={'placeholder': 'Имя пользователя', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        errors = []

        if self.instance.id:
            if User.objects.filter(username=username).exclude(id=self.instance.id).exists():
                self.add_error('username', 'Пользователь с таким именем уже существует.')
        else:
            if User.objects.filter(username=username).exists():
                self.add_error('username', 'Пользователь с таким именем уже существует.')

        if password and len(password) < 3:
            errors.append('Введённый пароль слишком короткий. Он должен содержать как минимум 3 символа.')

        if password != confirm_password:
            errors.append('Пароли не совпадают.')

        if errors:
            msg = " ".join(errors)
            self.fields['confirm_password'].help_text = f"{msg}Для подтверждения введите, пожалуйста, пароль ещё раз."
            for error in errors:
                self.add_error('confirm_password', error)
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
