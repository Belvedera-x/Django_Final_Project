from django.urls import path

from homefinder_app.views.reviews import ReviewCreateView, ReviewListView

urlpatterns = [
    path('<int:listing_id>/', ReviewListView.as_view()),
    path('create/', ReviewCreateView.as_view()),
]