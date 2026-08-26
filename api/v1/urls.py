from django.urls import path, include


app_name = 'v1'

urlpatterns = [
    # Inclui as URLs de cada app da versão 1
    path('', include('accounts.urls')),
    path('', include('sheets.urls')),
    path('', include('dice.urls')),
]
