from django.urls import path
from . import views

app_name = 'roll_dice'

urlpatterns = [
    path('dice/rolls/base/', views.roll_base_dice, name='roll_base'),
]
