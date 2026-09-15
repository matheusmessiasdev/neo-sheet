from drf_jsonschema.validators import JsonSchemaFieldValidator
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers
from .models import ProfileModel
# from .services.schema import BASE_SCHEMA_DEFAULTS, BASE_SCHEMA_FIELDS
from .services.profile_template import SCHEMAS_JSON_SCHEMA
from .services.resolved_schemas import resolve_schemas


def check_profile_default(data):
    # TODO check when default is used and, if it is and it is false,
    # custom schema must be within it
    ...


@extend_schema_field(OpenApiTypes.OBJECT)
class SchemasJSONField(serializers.JSONField):
    """
    JSONField that drf-spectacular documents as 'object' instead of 'any'.
    """
    pass


class ProfileSerializer(serializers.ModelSerializer):
    schemas = SchemasJSONField(default=dict,
                               validators=[JsonSchemaFieldValidator(schema=SCHEMAS_JSON_SCHEMA)])

    class Meta:
        model = ProfileModel
        fields = ['system_id', 'display_name', 'schemas', 'is_official']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['schemas'] = resolve_schemas(instance.schemas)
        return data


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ['system_id', 'display_name',]
