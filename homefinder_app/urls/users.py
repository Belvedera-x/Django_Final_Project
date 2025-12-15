from django.urls import path

from homefinder_app.views.users import RegisterUser




urlpatterns = [
    path('register/', RegisterUser.as_view()),
]