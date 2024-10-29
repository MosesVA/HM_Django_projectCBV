import random
import string

from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.views.generic import CreateView, UpdateView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from users.models import User
from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserPasswordChangeForm
from users.services import send_register_mail, send_new_password


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login_user')
    template_name = 'users/register_user.html'


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login_user.html'


@login_required
def user_profile_view(request):
    user_object = request.user
    context = {
        'title': f'Ваш профиль {user_object.first_name}',
    }
    return render(request, 'users/user_profile_read_only.html', context)


@login_required
def user_update_view(request):
    user_object = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user_object)
        if form.is_valid():
            user_object = form.save()
            user_object.save()
            return HttpResponseRedirect(reverse('users:profile_user'))
    user_name = user_object.first_name
    context = {
        'object': user_object,
        'title': f'Изменить профиль {user_name}',
        'form': UserUpdateForm(instance=user_object)
    }
    return render(request, 'users/update_user.html', context)


@login_required
def user_change_password_view(request):
    user_object = request.user
    form = UserPasswordChangeForm(user_object, request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user_object = form.save()
            update_session_auth_hash(request, user_object)
            messages.success(request, 'Пароль был успешно изменен!')
            return HttpResponseRedirect(reverse('users:profile_user'))
        else:
            messages.error(request, 'Не удалось изменить пароль!')
    context = {
        'form': form
    }
    return render(request, 'users/change_password_user.html', context)


# class UserPasswordChangeView(PasswordChangeView):
#     form_class = UserPasswordChangeForm
#     success_url = reverse_lazy('users:profile_user')
#     template_name = 'users/change_password_user.html'


def user_logout_view(request):
    logout(request)
    return redirect('dogs:index')


@login_required
def user_generate_new_password(request):
    new_password = ''.join(random.sample((string.ascii_letters + string.digits), 12))
    request.user.set_password(new_password)
    request.user.save()
    send_new_password(request.user.email, new_password)
    return redirect(reverse('dogs:index'))
