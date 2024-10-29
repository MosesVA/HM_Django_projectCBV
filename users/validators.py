import re

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_password(field):
    pattern = re.compile(r'^[A-Za-z0-9]+$')
    language = settings.LANGUAGE_CODE
    error_messages = [
        {
            'ru-ru': 'Пароль должен содержать только буквы латинского алфавита и цифры!',
            'en-us': 'Must contain A-Z, a-z letters and 0-9 numbers!'
        },
        {
            'ru-ru': 'Длина пароля должна быть между 8 и 16 символами!',
            'en-us': 'Password length must be between 8 and 16 characters!'
        }
    ]
    if not bool(re.match(pattern, field)):
        raise ValidationError(error_messages[0][language], code=error_messages[0][language])
    if not 8 <= len(field) <= 16:
        raise ValidationError(error_messages[1][language], code=error_messages[1][language])
