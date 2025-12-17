from django.urls import path

from homefinder_app.views.reviews import ReviewCreateView, ReviewListView

urlpatterns = [
    path('reviews/<int:housing_id>/', ReviewListView.as_view()),
    path('housings/<int:housing_id>/reviews/', ReviewCreateView.as_view()),
]