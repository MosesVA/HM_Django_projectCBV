from datetime import datetime

from django import forms

from dogs.models import Dog, Parent
from users.forms import StyleFormMixin


class DogForm(StyleFormMixin, forms.ModelForm):
    """Форма собаки"""

    class Meta:
        model = Dog
        exclude = ('owner', 'is_active', 'views')

    def clean_birth_date(self):
        """Переписан метод clean_birth_date(), теперь если собака
        старше 100 лет ее создание/изменение будет невозможно"""
        if self.cleaned_data['birth_date']:
            cleaned_data = self.cleaned_data['birth_date']
            now_year = datetime.now().year
            if now_year - cleaned_data.year > 100:
                raise forms.ValidationError('Собака не может быть старше 100 лет')
            return cleaned_data
        return


class DogAdminForm(StyleFormMixin, forms.ModelForm):
    """Форма собаки для Админа"""
    class Meta:
        model = Dog
        fields = '__all__'

    def clean_birth_date(self):
        """Переписан метод clean_birth_date(), теперь если собака
        старше 100 лет ее создание/изменение будет невозможно"""
        if self.cleaned_data['birth_date']:
            cleaned_data = self.cleaned_data['birth_date']
            now_year = datetime.now().year
            if now_year - cleaned_data.year > 100:
                raise forms.ValidationError('Собака не может быть старше 100 лет')
            return cleaned_data
        return


class ParentForm(StyleFormMixin, forms.ModelForm):
    """Форма родителей собаки"""
    class Meta:
        model = Parent
        fields = '__all__'
