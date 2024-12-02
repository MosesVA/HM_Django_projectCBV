from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm

from users.models import User
from users.validators import validate_password


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserForm(StyleFormMixin, forms.ModelForm):
    """Форма Пользователя"""
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar')


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Форма регистрации Пользователя"""
    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        """Переписан метод clean_password2()
        для внедрения собственного валидатора"""
        cd = self.cleaned_data
        validate_password(cd['password1'])
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('password_mismatch')
        return cd['password2']


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    """Форма входа в профиль пользователя(стандарт джанго)"""
    pass


class UserUpdateForm(StyleFormMixin, forms.ModelForm):
    """Форма обновления данных Пользователя"""
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'telegram', 'avatar')


class UserPasswordChangeForm(StyleFormMixin, PasswordChangeForm):
    """Форма смены пароля Пользователя"""
    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        validate_password(password1)
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        password_validation.validate_password(password2, self.user)
        return password2
