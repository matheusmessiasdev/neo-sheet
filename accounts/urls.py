from django.urls import path, include
from . import views
from rest_framework import routers

# app_name = 'all_users'


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
