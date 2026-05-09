from drf_jsonschema.validators import JsonSchemaFieldValidator
from rest_framework import serializers
from .models import ProfileModel
from .services.schema import BASE_SCHEMA_DEFAULTS, BASE_SCHEMA_FIELDS
from .services.profile_template import PROFILE_TEMPLATE_SCHEMA, SCHEMAS_JSON_SCHEMA
from copy import deepcopy


def check_profile(data):
    ...


class ProfileSerializer(serializers.ModelSerializer):
    schemas = serializers.JSONField(default=dict, validators=[
                                    JsonSchemaFieldValidator(schema=SCHEMAS_JSON_SCHEMA)])

    class Meta:
        model = ProfileModel
        fields = ['system_id', 'display_name', 'schemas',]
