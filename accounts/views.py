from django.shortcuts import render
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from djoser.views import UserViewSet
# Create your views here.


@method_decorator(ratelimit(key='ip', rate=settings.RATELIMITS['login'], method='POST', block=True), name='post')
class RateLimitedTokenObtainPairView(TokenObtainPairView):
    """Extends the simplejwt login view to add IP rate limiting"""
    pass


class UsersViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    ...


@method_decorator(ratelimit(key='ip', rate=settings.RATELIMITS['register'], method='POST', block=True), name='create')
class RateLimitedUserViewSet(UserViewSet):
    """Extends the UserViewSet from djoser to add rate limiting to the register"""
    pass
