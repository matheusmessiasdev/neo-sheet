from django.urls import path, include
from proto_sheet.health import health_check

app_name = 'v1'

urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('', include('accounts.urls')),
    path('', include('sheets.urls')),
    path('', include('dice.urls')),
]
