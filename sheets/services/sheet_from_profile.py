from ..models import ProfileModel
from .schema import BASE_SCHEMA_FIELDS, BASE_SCHEMA_DEFAULTS
from rest_framework.exceptions import bad_request
from copy import deepcopy
import re

base_fields_and_label = deepcopy(BASE_SCHEMA_FIELDS)
base_fields_and_label.append('label')


def configure_sheet_from_profile2(profile: ProfileModel):
    sheet = BASE_SCHEMA_DEFAULTS
    profile_schemas = profile.schemas
    print(profile_schemas)
    for key, schema in profile_schemas.items():
        key_schema_list = [
            (key, item) for item in BASE_SCHEMA_FIELDS if re.search(item, key)]
    for items in key_schema_list:
        key,
    ...


def configure_sheet_from_profile(profile: ProfileModel):
    sheet = BASE_SCHEMA_DEFAULTS
    profile_schemas = profile.schemas
    profile_schemas_keys = profile_schemas.keys()
    PATTERN = r'^([^_]+)'

    RE_MATCH = [re.search(PATTERN, key).group(1)
                for key in profile_schemas_keys if re.search(PATTERN, key)]
    profile_field_schema_pair = list(zip(RE_MATCH, profile_schemas_keys))

    for field, schema_key in profile_field_schema_pair:
        default_field = sheet[field]
        schema = profile_schemas[schema_key]
        schema_default = schema.get('default')
        print(default_field, 'antes')

        if not schema_default and schema_default is not None:
            print(schema_default, 'VALOR DE DEFAULT')
            default_field = schema.get('custom_schema')
            new_default_field = strip_metadata(default_field)
            print(default_field, 'depois')
            sheet[field] = new_default_field

        # Lists are set to get the base schema from template
        if isinstance(default_field, list):
            list_field = default_field
            default_field = default_field[0]

        if schema.get('added_fields'):
            new_added_fields = strip_metadata(schema.get('added_fields'))
            print(new_added_fields, 'NEW ADDED FIELDS')
            default_field.update(new_added_fields)

        if schema.get('field_overrides'):
            new_field_overrides = strip_metadata(schema.get('field_overrides'))
            for field, field_value in new_field_overrides.items():
                if field_value:
                    default_field.update(new_field_overrides)
                    continue

                # default_field.pop(field)
    print('FINAL SHEET')
    print('FINAL SHEET')
    print('FINAL SHEET')
    print('FINAL SHEET')
    print(sheet)
    ...

    ...


def strip_metadata(obj):
    """
    Remove recursivamente todas as chaves que começam com '_'
    de dicionários e listas.
    """
    if isinstance(obj, dict):
        # Cria um novo dicionário sem as chaves metadados
        return {
            key: strip_metadata(value)
            for key, value in obj.items()
            if not key.startswith('_')
        }
    elif isinstance(obj, list):
        # Processa cada item da lista
        return [strip_metadata(item) for item in obj]
    else:
        # Valores simples (str, int, bool, None) retornam intactos
        return obj
