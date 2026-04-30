from django.urls import path
from . import views

app_name = 'v1'

urlpatterns = [
    path('dice/rolls/base', views.roll_base_dice, name='roll_base'),
]
