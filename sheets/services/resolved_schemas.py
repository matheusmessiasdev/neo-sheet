from .profile_template import PROFILE_BLANK_SCHEMA
from copy import deepcopy


def resolve_schemas(schema: dict):
    old_profile = deepcopy(PROFILE_BLANK_SCHEMA)
    new_schema = old_profile.get('schemas')

    instance_schemas_keys = schema.keys()

    for schema_key in instance_schemas_keys:
        new_schema[schema_key] = schema[schema_key]
    return new_schema
# TODO adicionar os metadados do que exatamente foi adicionado
