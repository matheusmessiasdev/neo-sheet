from django.urls import path, include
from . import views
from rest_framework import routers


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
