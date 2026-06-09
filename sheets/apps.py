from django.apps import AppConfig
from django.db.models.signals import pre_save

class SheetsConfig(AppConfig):
    name = 'sheets'