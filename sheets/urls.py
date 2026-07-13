from django.urls import path
from . import views
from rest_framework import routers

app_name = 'all_sheets'

router = routers.DefaultRouter()
router.register(r'profiles', views.ProfilesViewSet)

urlpatterns = router.urls
# TODO configurar o SHEETS endpoint
# TODO configurar o PATCH
# urlpatterns = [
#     path('profiles/', views.ProfilesList.as_view(), name='profile_list'),
#     path('profiles/blank/', views.blank_profile, name='blank_profile'),
#     path('profiles/template/', views.profile_template, name='profile_template'),
#     path('profiles/create/', views.profiles, name='profile_template'),
#     path('profiles/generic/', views.blank_sheet, name='generic_sheet'),
#     path('profiles/<str:system_id>/sheet',
#          views.sheet_from_profile, name='profile_detail'),
#     path('profiles/<str:system_id>/', views.show_profile, name='profile_detail'),
# ]
