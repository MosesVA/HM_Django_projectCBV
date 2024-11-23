import random
import string

from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.shortcuts import reverse, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from users.models import User
from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserPasswordChangeForm, UserForm
from users.services import send_register_mail, send_new_password


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login_user')
    template_name = 'users/register_user.html'

    def form_valid(self, form):
        self.object = form.save()
        send_register_mail(self.object.email)
        return super().form_valid(form)


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login_user.html'


class UserProfileView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_profile_read_only.html'

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update_user.html'
    success_url = reverse_lazy('users:profile_user')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/change_password_user.html'
    success_url = reverse_lazy('users:profile_user')


class UserLogoutView(LogoutView):
    template_name = 'users/logout_user.html'


class UserListView(LoginRequiredMixin, ListView):
    model = User
    extra_context = {
        'title': 'Питомник - Все наши заводчики'
    }
    template_name = 'users/users.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


class UserViewProfileView(DetailView):
    model = User
    template_name = 'users/user_view_profile.html'


@login_required
def user_generate_new_password(request):
    new_password = ''.join(random.sample((string.ascii_letters + string.digits), 12))
    request.user.set_password(new_password)
    request.user.save()
    send_new_password(request.user.email, new_password)
    return redirect(reverse('dogs:index'))
