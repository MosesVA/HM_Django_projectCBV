from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from dogs.views import index, DogListView, DogCreateView, DogDetailView, DogUpdateView, \
    DogDeleteView, DogCategoryListView, CategoryListView, DogDeactivateListView, dog_toggle_activity
from dogs.apps import DogsConfig

app_name = DogsConfig.name

urlpatterns = [
    path('', cache_page(60)(index), name='index'),
    path('categories/', cache_page(60)(CategoryListView.as_view()), name='categories'),
    path('categories/<int:pk>/dogs/', DogCategoryListView.as_view(), name='category_dogs'),
    path('dogs/', DogListView.as_view(), name='list_dogs'),
    path('dogs/deactivate', DogDeactivateListView.as_view(), name='deactivated_list_dogs'),
    path('dogs/create/', DogCreateView.as_view(), name='create_dog'),
    path('dogs/detail/<int:pk>/', DogDetailView.as_view(), name='detail_dog'),
    path('dogs/update/<int:pk>/', never_cache(DogUpdateView.as_view()), name='update_dog'),
    path('dogs/toggle/<int:pk>/', dog_toggle_activity, name='toggle_activity_dog'),
    path('dogs/delete/<int:pk>/', DogDeleteView.as_view(), name='delete_dog')
]
