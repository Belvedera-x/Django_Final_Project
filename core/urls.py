"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from homefinder_app.views.housings import (
    HousingToggleAvailableView,
    HousingCreateView,
    HousingUpdateView
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('housing/', HousingToggleAvailableView.as_view()),
    path('housing/create/', HousingCreateView.as_view()),
    path('housing/<int:pk>/update', HousingUpdateView.as_view()),
    path('housing/<int:pk>/toggle-available/', HousingToggleAvailableView.as_view()),
]
