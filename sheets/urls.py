from django.urls import path
from . import views

app_name = 'all_sheets'

urlpatterns = [
    path('profiles/template/blank/', views.blank_profile, name='blank_profile'),
    path('profiles/template/', views.profile_template, name='profile_template'),
    path('profiles/create/', views.profiles, name='profile_template'),
    path('profiles/generic/', views.blank_sheet, name='generic_sheet'),
]
