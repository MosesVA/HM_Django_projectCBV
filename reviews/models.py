from django.db import models
from django.conf import settings
from django.urls import reverse

from users.models import NULLABLE
from dogs.models import Dog


class Review(models.Model):
    """Модель отзыва о собаке"""
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.SlugField(max_length=25, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(verbose_name='Содержимое')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    sign_of_review = models.BooleanField(default=True, verbose_name='активный')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Автор')
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='dogs', verbose_name='Собака')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('reviews:detail_review', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'reviews'
