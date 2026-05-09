from .schema import BASE_SCHEMA_DEFAULTS, BASE_SCHEMA_FIELDS
from .profile_template import PROFILE_TEMPLATE_SCHEMA
from copy import deepcopy


def profile_validator(data):
    base_schema_fields = deepcopy(BASE_SCHEMA_DEFAULTS)
    ...
