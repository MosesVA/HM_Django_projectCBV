from django.urls import path

from dogs.views import index, categories, category_dogs, dog_detail_view, \
    dog_update_view, dog_delete_view, DogListView, DogCreateView
from dogs.apps import DogsConfig

app_name = DogsConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('categories/', categories, name='categories'),
    path('categories/<int:pk>/dogs/', category_dogs, name='category_dogs'),
    path('dogs/', DogListView.as_view(), name='list_dogs'),
    path('dogs/create/', DogCreateView.as_view(), name='create_dog'),
    path('dogs/detail/<int:pk>/', dog_detail_view, name='detail_dog'),
    path('dogs/update/<int:pk>/', dog_update_view, name='update_dog'),
    path('dogs/delete/<int:pk>/', dog_delete_view, name='delete_dog')
]
