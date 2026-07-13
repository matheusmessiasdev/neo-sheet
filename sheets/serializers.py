from drf_jsonschema.validators import JsonSchemaFieldValidator
from rest_framework import serializers
from .models import ProfileModel
# from .services.schema import BASE_SCHEMA_DEFAULTS, BASE_SCHEMA_FIELDS
from .services.profile_template import PROFILE_TEMPLATE_SCHEMA, SCHEMAS_JSON_SCHEMA
from .services.resolved_schemas import resolve_schemas


def check_profile_default(data):
    # TODO check when default is used and, if it is and it is false,
    # custom schema must be within it
    ...


class ProfileSerializer(serializers.ModelSerializer):
    schemas = serializers.JSONField(default=dict,
                                    validators=[JsonSchemaFieldValidator(schema=SCHEMAS_JSON_SCHEMA)])

    class Meta:
        model = ProfileModel
        fields = ['system_id', 'display_name', 'schemas',]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['schemas'] = resolve_schemas(instance.schemas)
        return data


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ['system_id', 'display_name',]
