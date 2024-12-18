from django.http import HttpResponseForbidden
from django.shortcuts import reverse, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied

from reviews.models import Review
from reviews.forms import ReviewForm
from users.models import UserRoles
from reviews.utils import slug_generator


class ReviewListView(LoginRequiredMixin, ListView):
    """Отрисовка страницы со всеми отзывами"""
    model = Review
    paginate_by = 2
    extra_context = {
        'title': 'Все отзывы'
    }
    template_name = 'reviews/reviews_list.html'

    def get_queryset(self):
        """Переписан метод get_queryset() для сортировки активных отзывов"""
        queryset = super().get_queryset()
        queryset = queryset.filter(sign_of_review=True)
        return queryset


class ReviewDeactivatedListView(LoginRequiredMixin, ListView):
    """Отрисовка страницы со всеми неактивными отзывами"""
    model = Review
    paginate_by = 2
    extra_context = {
        'title': 'Неактивные отзывы'
    }
    template_name = 'reviews/reviews_list.html'

    def get_queryset(self):
        """Переписан метод get_queryset() для сортировки неактивных собак
        (владельцу показывает только его собаку)"""
        queryset = super().get_queryset()
        queryset = queryset.filter(sign_of_review=False)
        return queryset


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """Отрисовка страницы создания отзыва"""
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_create_update.html'

    def form_valid(self, form):
        if self.request.user.role not in [UserRoles.USER, UserRoles.ADMIN]:
            return HttpResponseForbidden()
        self.object = form.save()
        print(self.object.slug)
        if self.object.slug == 'temp_slug':
            self.object.slug = slug_generator()
            print(self.object.slug)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    """Отрисовка страницы обновления данных отзыва"""
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_create_update.html'

    def get_success_url(self):
        return reverse('reviews:detail_review', args=[self.kwargs.get('slug')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.author != self.request.user and self.request.user not in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            raise PermissionDenied()
        return self.object


class ReviewDetailView(LoginRequiredMixin, DetailView):
    """Отрисовка страницы деталей об отзыве"""
    model = Review
    template_name = 'reviews/review_detail.html'


class ReviewDeleteView(PermissionRequiredMixin, DeleteView):
    """Отрисовка страницы удаления отзыва"""
    model = Review
    template_name = 'reviews/review_delete.html'
    permission_required = 'reviews.delete_review'

    def get_success_url(self):
        return reverse('reviews:list_reviews')


def review_toggle_activity(request, slug):
    """Отрисовка страницы с активными или неактивными отзывами"""
    review_item = get_object_or_404(Review, slug=slug)
    if review_item.sign_of_review:
        review_item.sign_of_review = False
        review_item.save()
        return redirect(reverse('reviews:deactivated_reviews'))
    else:
        review_item.sign_of_review = True
        review_item.save()
        return redirect(reverse('reviews:list_reviews'))
