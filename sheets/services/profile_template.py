from .schema import BASE_SCHEMA_FIELDS
PROFILE_TEMPLATE_SCHEMA = {
    "system_id": '',
    "display_name": '',

    "field_map": {
        "_description": 'Map Base Fields to labels in your system.',
        "_example": {
            "spells": {'label': 'Rituals', 'key': 'spells'}
        },
    },
    "active_fields": {
        "_description": 'List avaliable fields in your  system.',
        "_fields_avaliable": BASE_SCHEMA_FIELDS,
        "_value": [],
    },
    "inactive_fields": {
        "_description": 'List unavaliable fields in your  system.',
        "_value": [],
    },
    "field_overrides": {
        "_description": 'Redefine the internal structure of base fields.',
        "_example": {
            "defenses": {
                "saving_throws": None
            }
        },
    },
    "attributes_schema": {
        "_description": "Declare your system's attributes with limits.",
        "_example": {
            "attributes": {"label": "Strength", "min": 0, "max": 30}
        },
    },
    "status_schema": {
        "_description": "Declare your system's trackable resources with current/max.",
        "_example": {
            "health": {"label": "Life Points", "current": 0, "max": 100}
        },
    },
}
