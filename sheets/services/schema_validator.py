from ..models import ProfileModel
from .schema import BASE_SCHEMA_FIELDS
from rest_framework.exceptions import bad_request
from copy import deepcopy


def schema_validator(system_id):
    flag = False
    try:
        profile = ProfileModel.objects.get(system_id=system_id)
    except ProfileModel.DoesNotExist:
        return flag

    for key, value in profile.field_map.items():
        if key not in BASE_SCHEMA_FIELDS:
            return flag
        flag = 'label' in value and 'key' in value
        if not flag:
            return flag

    if profile.inactive_fields:
        flag = all(
            field in BASE_SCHEMA_FIELDS for field in profile.inactive_fields
        )
    else:
        flag = True
    if not flag:
        return flag

    if profile.field_overrides:
        for key, value in profile.field_overrides.items():
            print(key, value)
            print(value)
            flag = key in BASE_SCHEMA_FIELDS and isinstance(value, dict) \
                or isinstance(value, list)
            if not flag:
                return flag
    else:
        return (f'A ficha ta certinha.')
# TODo corrigir field_overrides dando erro quando não devia (ver print)
