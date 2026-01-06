from django.urls import path, include
from rest_framework.routers import DefaultRouter

from homefinder_app.views.bookings import BookingViewSet
from homefinder_app.views.housings import HousingViewSet

from homefinder_app.views.users import RegisterUser, UserLoginAPIView, LogOutUser

router = DefaultRouter()
router.register('housings', HousingViewSet)
router.register('bookings', BookingViewSet)


urlpatterns = [
    path('', include('homefinder_app.urls.reviews')),

    # login \ logout
    path('auth/register/', RegisterUser.as_view()),
    path('auth/login/', UserLoginAPIView.as_view()),
    path('auth/logout/', LogOutUser.as_view()),
] + router.urls