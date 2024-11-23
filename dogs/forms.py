from datetime import datetime

from django import forms

from dogs.models import Dog, Parent
from users.forms import StyleFormMixin


class DogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Dog
        exclude = ('owner', 'is_active', 'views')

    def clean_birth_date(self):
        if self.cleaned_data['birth_date']:
            cleaned_data = self.cleaned_data['birth_date']
            now_year = datetime.now().year
            if now_year - cleaned_data.year > 100:
                raise forms.ValidationError('Собака не может быть старше 100 лет')
            return cleaned_data
        return


class DogAdminForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Dog
        fields = '__all__'

    def clean_birth_date(self):
        if self.cleaned_data['birth_date']:
            cleaned_data = self.cleaned_data['birth_date']
            now_year = datetime.now().year
            if now_year - cleaned_data.year > 100:
                raise forms.ValidationError('Собака не может быть старше 100 лет')
            return cleaned_data
        return


class ParentForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Parent
        fields = '__all__'
