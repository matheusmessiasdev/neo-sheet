from ..models import ProfileModel
from .schema import BASE_SCHEMA_FIELDS
from rest_framework.exceptions import bad_request
from copy import deepcopy

base_fields_and_label = deepcopy(BASE_SCHEMA_FIELDS)
base_fields_and_label.append('label')


def configure_sheet_from_profile(system_id):
    ...
