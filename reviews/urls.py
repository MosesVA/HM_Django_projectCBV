from django.urls import path

from reviews.views import DogReviewListView, DeactivatedDogReviewListView
from reviews.apps import ReviewsConfig

app_name = ReviewsConfig.name

urlpatterns = [
    path('<int:pk>/reviews/', DogReviewListView.as_view(), name='reviews_list'),
    path('<int:pk>/reviews/deactivated', DeactivatedDogReviewListView.as_view(), name='deactivated_reviews_list')
]
