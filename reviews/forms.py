from django import forms

from models import Review
from dogs.forms import StyleFormMixin


class ReviewForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Review
        include = ('dog', 'title', 'content', 'slug')
