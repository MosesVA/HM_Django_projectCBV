from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail

from dogs.models import Category, Dog


def get_categories_cache():
    if settings.CACHE_ENABLED:
        key = 'category_list'
        category_list = cache.get(key)
        if category_list is None:
            category_list = Category.objects.all()
            cache.set(key, category_list)
    else:
        category_list = Category.objects.all()
    return category_list


def send_views_mail(dog_object, owner_email, views_count):
    send_mail(
        subject=f'{views_count} просмотров {dog_object}',
        message=f'Юхуу! Уже {views_count} просмотров {dog_object}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[owner_email, ]
    )
