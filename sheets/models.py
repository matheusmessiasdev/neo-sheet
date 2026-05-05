from django.db import models

# Create your models here.


class ProfileTemplate(models.Model):
    system_id = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)

    field_map = models.JSONField(default=dict)
    active_fields = models.JSONField(default=dict)
    inactive_fields = models.JSONField(default=dict)
    field_overrides = models.JSONField(default=dict)

    class Meta:
        ordering = ['system_id']
    ...

    def __str__(self):
        return self.display_name
