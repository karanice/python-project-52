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
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Хэширование пароля
        if commit:
            user.save()
        return user
