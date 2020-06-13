"""ips URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from pages.views import home_view
from person.views import person_view
from locations.views import (
    livelocations_view, 
    heatmap_view, 
    usertraces_view, 
    usertraces_main_view
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('home/', home_view, name='home'),
    path('livelocations/', livelocations_view, name='livelocations'),
    path('heatmap/', heatmap_view, name='heatmap'),
    path('usertraces-main/', usertraces_main_view, name='usertraces'),
    path('usertraces/<str:person_id>/', usertraces_view, name='usertraces'),
    path('person/<str:person_id>/', person_view, name='person')
]
