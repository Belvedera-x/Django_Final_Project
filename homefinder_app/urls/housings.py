from django.urls import path

from homefinder_app.views.housings import HousingToggleAvailableView


urlpatterns = [
    path('housings/<int:pk>/toggle-available/', HousingToggleAvailableView.as_view()),
]