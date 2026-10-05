from .profile_template import PROFILE_BLANK_SCHEMA
from copy import deepcopy


def resolve_schemas(schema: dict):
    old_profile = deepcopy(PROFILE_BLANK_SCHEMA)
    new_schema = old_profile.get('schemas')

    added_schemas = {}
    for schema_key in schema.keys():

        added_schemas[schema_key] = schema[schema_key]
        new_schema[schema_key] = schema[schema_key]

    new_schema['_meta'] = {'added_schemas': added_schemas}

    return new_schema
