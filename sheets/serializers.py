from rest_framework import serializers
from .models import ProfileTemplateModel


class ProfileTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileTemplateModel
        fields = ['system_id', 'display_name', 'field_map', 'active_fields',
                  'inactive_fields', 'field_overrides', 'custom_fields',]
    ...
