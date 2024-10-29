from django.db import models
from django.conf import settings

from users.models import NULLABLE


class Category(models.Model):
    """Модель 'Категория' собак"""
    name = models.CharField(max_length=100, verbose_name='breed')
    description = models.CharField(max_length=1000, verbose_name='description')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'breed'
        verbose_name_plural = 'breeds'


class Dog(models.Model):
    """Модель 'Собака'"""
    name = models.CharField(max_length=250, verbose_name='dog_name')
    # category = models.CharField(max_length=100, verbose_name='breed')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='breed')
    photo = models.ImageField(upload_to='dogs/', **NULLABLE, verbose_name='image')
    birth_date = models.DateField(**NULLABLE, verbose_name='birth_date')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='Владелец')

    def __str__(self):
        return f'{self.name} ({self.category})'

    class Meta:
        verbose_name = 'dog'
        verbose_name_plural = 'dogs'
