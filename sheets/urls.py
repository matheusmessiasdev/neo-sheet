from django.urls import path
from . import views

app_name = 'all_sheets'

urlpatterns = [
    path('profiles/', views.ProfilesList.as_view(), name='profile_list'),
    path('profiles/blank/', views.blank_profile, name='blank_profile'),
    path('profiles/template/', views.profile_template, name='profile_template'),
    path('profiles/generic/', views.generic_sheet, name='generic_sheet'),
    path('profiles/<str:system_id>/sheet',
         views.sheet_from_profile, name='profile_detail'),
    path('profiles/<str:system_id>/', views.show_profile, name='profile_detail'),
]
