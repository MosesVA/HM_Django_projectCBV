from django.urls import path

from reviews.views import ReviewListView, ReviewDeactivatedListView
from reviews.apps import ReviewsConfig

app_name = ReviewsConfig.name

urlpatterns = [
    path('', ReviewListView.as_view(), name='list_reviews'),
    path('deactivated/', ReviewDeactivatedListView.as_view(), name='deactivated_reviews')
]
