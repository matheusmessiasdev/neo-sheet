from django.urls import path
from . import views
from rest_framework import routers

# app_name = 'all_sheets'

router = routers.SimpleRouter()
router.register(r'profiles', views.ProfilesViewSet, basename='profile')

urlpatterns = router.urls
