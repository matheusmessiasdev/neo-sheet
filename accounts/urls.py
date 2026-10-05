from django.urls import path, include
from . import views


urlpatterns = [
    path('auth/jwt/create/',
         views.RateLimitedTokenObtainPairView.as_view(), name='jwt-create'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
