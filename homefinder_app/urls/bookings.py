from django.urls import path

from homefinder_app.views.bookings import BookingListView, BookingCreateView

urlpatterns = [
    path('', BookingListView.as_view()),
    path('create/', BookingCreateView.as_view()),
]