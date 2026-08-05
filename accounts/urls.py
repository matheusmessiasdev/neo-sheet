from django.urls import path
from . import views
from rest_framework import routers

app_name = 'all_users'

router = routers.DefaultRouter()
router.register(r'users', views.UsersViewSet)

urlpatterns = router.urls
