from django.urls import path

from homefinder_app.views.housings import (
    HousingListView,
    HousingDeleteView,
    HousingUpdateView,
    HousingCreateView,
    HousingSearchView,
    HousingToggleAvailableView
)


urlpatterns = [
    path('', HousingListView.as_view()),
    path('available/', HousingSearchView.as_view()),
    path('create/', HousingCreateView.as_view()),
    path('<int:pk>/delete/', HousingDeleteView.as_view()),
    path('<int:pk>/update/', HousingUpdateView.as_view()),
    path('<int:pk>/toggle-available/', HousingToggleAvailableView.as_view()),
]