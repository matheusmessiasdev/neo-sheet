from django.urls import path
from . import views

app_name = 'all_sheets'

urlpatterns = [
    path('profiles/generic/', views.blank_sheet, name='generic_sheet'),
]
