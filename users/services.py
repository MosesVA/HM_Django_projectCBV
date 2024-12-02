from django.conf import settings
from django.core.mail import send_mail


def send_register_mail(email):
    """Функция отправки письма на почту пользователю
    после регистрации на сайте"""
    send_mail(
        subject='Поздравляем с регистрацией!',
        message='Вы успешно зарегистрировались на нашей платформе! Добро пожаловать!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )


def send_new_password(email, new_password):
    """Функция отправки письма на почту пользователю
    после смены пароля"""
    send_mail(
        subject='Вы успешно сменили пароль!',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
