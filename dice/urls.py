from django.urls import path
from . import views
urlpatterns = [
    path('', views.roll_base_dice),
]
