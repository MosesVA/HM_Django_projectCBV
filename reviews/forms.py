from django import forms

from reviews.models import Review
from dogs.forms import StyleFormMixin


class ReviewForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Review
        fields = ('dog', 'title', 'content', 'slug')
