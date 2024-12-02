from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from dogs.models import Category, Dog, Parent
from dogs.forms import DogForm, DogAdminForm, ParentForm
from users.models import UserRoles
from dogs.services import send_views_mail


def index(request):
    """Отрисовка главной страницы сайта"""
    context = {
        'object_list': Category.objects.all()[:3],
        'title': 'Питомник - Главная'
    }
    return render(request, 'dogs/index.html', context)


class CategoryListView(LoginRequiredMixin, ListView):
    """Отрисовка страницы со всеми породами собак"""
    model = Category
    extra_context = {
        'title': 'Питомник - Все наши породы'
    }
    template_name = 'dogs/categories.html'


class CategorySearchListView(LoginRequiredMixin, ListView):
    """Отрисовка страницы поиска по категориям собак"""
    model = Category
    template_name = 'dogs/categories.html'
    extra_context = {
        'title': 'Результаты поиска'
    }

    def get_queryset(self):
        """Переписан метод get_queryset() для сортировки в соответствии с поисковым запросом"""
        query = self.request.GET.get('q')
        object_list = Category.objects.filter(
            Q(name__icontains=query),
        )
        return object_list


class DogCategoryListView(LoginRequiredMixin, ListView):
    """Отрисовка страницы с собаками отдельной категории"""
    model = Dog
    template_name = 'dogs/dogs.html'

    def get_queryset(self):
        """Переписан метод get_queryset() для сортировки активных собак"""
        queryset = super().get_queryset().filter(
            category_id=self.kwargs.get('pk'), is_active=True
        )

        # if not self.request.user.is_staff:
        #     queryset = queryset.filter(owner=self.request.user)

        return queryset


class DogListView(LoginRequiredMixin, ListView):
    """Отрисовка страницы со всеми активными собаками"""
    model = Dog
    paginate_by = 3
    extra_context = {
        'title': 'Питомник - Все наши собаки'
    }
    template_name = 'dogs/dogs.html'

    def get_queryset(self):
        """Переписан метод get_queryset() для сортировки активных собак"""
        queryset = super().get_queryset().filter(is_active=True)
        return queryset


class DogDeactivateListView(LoginRequiredMixin, ListView):
    """Отрисовка страницы со всеми неактивными собаками"""
    model = Dog
    extra_context = {
        'title': 'Питомник - Неактивные собаки'
    }
    template_name = 'dogs/dogs.html'

    def get_queryset(self):
        """Переписан метод get_queryset() для сортировки неактивных собак
        (владельцу показывает только его собаку)"""
        queryset = super().get_queryset()

        if self.request.user.role in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            queryset = queryset.filter(is_active=False)
        if self.request.user.role == UserRoles.USER:
            queryset = queryset.filter(is_active=False, owner=self.request.user)

        return queryset


class DogSearchListView(LoginRequiredMixin, ListView):
    """Отрисовка страницы поиска кличке собаки"""
    model = Dog
    template_name = 'dogs/dogs.html'
    extra_context = {
        'title': 'Результаты поиска'
    }

    def get_queryset(self):
        """Переписан метод get_queryset() для сортировки в соответствии с поисковым запросом"""
        query = self.request.GET.get('q')
        object_list = Dog.objects.filter(
            Q(name__icontains=query), is_active=True
        )
        return object_list


class DogCreateView(LoginRequiredMixin, CreateView):
    """Отрисовка страницы создания собаки"""
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'
    success_url = reverse_lazy('dogs:list_dogs')

    def form_valid(self, form):
        """Переписан метод form_valid() чтобы не зарегистрированный
        пользователь не мог создать собаку"""
        if self.request.user.role != UserRoles.USER:
            raise PermissionDenied()
            # return HttpResponseForbidden('У вас нет прав доступа!')  # только если ожидается перенаправление
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class DogDetailView(DetailView):
    """Отрисовка страницы деталей о собаке"""
    model = Dog
    template_name = 'dogs/detail.html'

    def get_context_data(self, **kwargs):
        """Переписан метод get_context_data() для увеличения кол-ва просмотров собаки
        людьми кроме ее владельца. Отправление письма о просмотрах на почту владельцу"""
        context_data = super().get_context_data(**kwargs)
        object = self.get_object()
        context_data['title'] = f'{object.name} {object.category}'
        dog_object_increase = get_object_or_404(Dog, pk=object.pk)
        # if object.owner != self.request.user and self.request.user.role not in [UserRoles.ADMIN, UserRoles.MODERATOR]:
        if object.owner != self.request.user:
            dog_object_increase.views_count()
        if object.owner:
            object_owner_email = object.owner.email
            if dog_object_increase.views % 100 == 0 and dog_object_increase.views != 0:
                send_views_mail(dog_object_increase.name, object_owner_email, dog_object_increase.views)
        return context_data


class DogUpdateView(LoginRequiredMixin, UpdateView):
    """Отрисовка страницы обновления данных о собаке"""
    model = Dog
    template_name = 'dogs/create_update.html'

    def get_success_url(self):
        return reverse('dogs:detail_dog', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        # if self.object.owner != self.request.user and not self.request.user.is_staff:
        if self.object.owner != self.request.user and self.request.user.role != UserRoles.ADMIN:
            raise PermissionDenied()
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ParentFormset = inlineformset_factory(Dog, Parent, form=ParentForm, extra=1)
        if self.request.method == 'POST':
            formset = ParentFormset(self.request.POST, instance=self.object)
        else:
            formset = ParentFormset(instance=self.object)
        context_data['formset'] = formset
        return context_data

    def get_form_class(self):
        dog_forms = {
            'admin': DogAdminForm,
            'moderator': DogForm,
            'user': DogForm
        }
        user_role = self.request.user.role
        dog_form_class = dog_forms[user_role]
        return dog_form_class

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class DogDeleteView(PermissionRequiredMixin, DeleteView):
    """Отрисовка страницы удаления собаки"""
    model = Dog
    template_name = 'dogs/delete.html'
    success_url = reverse_lazy('dogs:list_dogs')
    permission_required = 'dogs.delete_dog'
    #  dogs.add_dog - PermissionRequiredMixin + CreateView
    #  dogs.change_dog - PermissionRequiredMixin + UpdateView
    #  dogs.view_dog - PermissionRequiredMixin + DetailView


def dog_toggle_activity(request, pk):
    """Отрисовка страницы с активными или неактивными собаками"""
    dog_item = get_object_or_404(Dog, pk=pk)
    if dog_item.is_active:
        dog_item.is_active = False
    else:
        dog_item.is_active = True
    dog_item.save()
    return redirect(reverse('dogs:list_dogs'))
