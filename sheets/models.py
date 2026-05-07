from django.db import models

# Create your models here.


class ProfileTemplateModel(models.Model):
    system_id = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    is_official = models.BooleanField(default=False)

    field_map = models.JSONField(default=dict, blank=True)
    active_fields = models.JSONField(default=list)
    inactive_fields = models.JSONField(default=list)
    field_overrides = models.JSONField(default=dict, blank=True)
    custom_fields = models.JSONField(default=dict, blank=True)

    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['display_name']
    ...

    def __str__(self):
        return self.display_name
