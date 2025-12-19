from django.urls import path, include
# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from homefinder_app.views.bookings import BookingViewSet
from homefinder_app.views.housings import HousingViewSet
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from homefinder_app.views.users import RegisterUser, UserLoginAPIView, LogOutUser

router = DefaultRouter()
router.register('housings', HousingViewSet)
router.register('bookings', BookingViewSet)


urlpatterns = [
    path('', include('homefinder_app.urls.housings')),
    path('', include('homefinder_app.urls.reviews')),

    # path('token-auth/', obtain_auth_token),
    # path('jwt-auth/', TokenObtainPairView.as_view()),
    # path('jwt-refresh/', TokenRefreshView.as_view()),

    # login \ logout
    path('auth/register/', RegisterUser.as_view()),
    path('auth/login/', UserLoginAPIView.as_view()),
    path('auth/logout/', LogOutUser.as_view()),
] + router.urls