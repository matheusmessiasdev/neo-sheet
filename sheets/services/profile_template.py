
PROFILE_TEMPLATE_SCHEMA = {
    "system_id": "",
    "display_name": "",
    "base_schema_url": "/api/v1/generic_sheet/",


    "schemas": {
        "_description": "The object templates for every aspect of your sheet. If default is false, you can use custom_schemas to create your own",

        "identity_schema": {
            "_description": "Your character's sheet information.",
            "default": True,
            "added_fields": {},
            "field_overrides": {},
            "custom_schema": {},
        },
        "attributes_schema": {
            "_description": "Your system's attributes with limits.",
            "default": True,
            "added_fields": {},
            "field_overrides": {},
            "custom_schema": {},
        },
        "status_schema": {
            "_description": "Your system's status (Life Points, Mana, Sanity).",
            "default": True,
            "added_fields": {},
            "field_overrides": {},
            "custom_schema": {},
        },
        "defense_schema": {
            "_description": "Your system's defense and resistance values.",
            "default": True,
            "added_fields": {},
            "field_overrides": {},
            "custom_schema": {},
        },
        "skills_item_schema": {
            "_description": "Your system's skills or similar variants.",
            "default": True,
            "added_fields": {},
            "field_overrides": {},
            "custom_schema": {},
        },
        "abilities_item_schema": {
            "_description": "Your system's abilities and talents.",
            "default": True,
            "added_fields": {},
            "field_overrides": {},
            "custom_schema": {},
        },
        "spells_item_schema": {
            "_description": "Your system's magic or similar variants.",
            "default": True,
            "added_fields": {},
            "field_overrides": {},
            "custom_schema": {},
        },
        "inventory_item_schema": {
            "_description": "Your system's inventory.",
            "default": True,
            "added_fields": {},
            "field_overrides": {},
            "custom_schema": {},
        },
        "custom_fields": {
            "_description": "Fields that does not exist in the base schema. Types: int, str, bool, object, list.",
            "added_fields": {
                "_mask": {
                    "default": {"name": "", "bonus": 0},
                    "abilities": {
                        "name": "",
                        "bonus": 0,
                        "description": 0
                    }
                },
                "_trauma_track": {
                    "saving_tests": [False, False, False],
                }
            }
        },
    },
}

PROFILE_BLANK_SCHEMA = {
    "system_id": "",
    "display_name": "",


    "schemas": {
        "identity_schema": {
            "default": True,
            "added_fields": {},
            "field_overrides": {},
            "custom_schema": {},
        },
        "attributes_schema": {
            "default": True,
            "added_fields": {},
            "field_overrides": {},
            "custom_schema": {},
        },
        "status_schema": {
            "default": True,
            "added_fields": {},
            "field_overrides": {},
            "custom_schema": {},
        },
        "defense_schema": {
            "default": True,
            "added_fields": {},
            "field_overrides": {},
            "custom_schema": {},
        },
        "skills_item_schema": {
            "default": True,
            "added_fields": {},
            "field_overrides": {},
            "custom_schema": {},
        },
        "abilities_item_schema": {
            "default": True,
            "added_fields": {},
            "field_overrides": {},
            "custom_schema": {},
        },
        "spells_item_schema": {
            "default": True,
            "added_fields": {},
            "field_overrides": {},
            "custom_schema": {},
        },
        "inventory_item_schema": {
            "default": True,
            "added_fields": {},
            "field_overrides": {},
            "custom_schema": {},
        },
        "custom_fields": {
            "added_fields": {},
        },
    }
}
SCHEMAS_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "identity_schema": {"$ref": "#/$defs/section_schema"},
        "attributes_schema": {"$ref": "#/$defs/section_schema"},
        "status_schema": {"$ref": "#/$defs/section_schema"},
        "defense_schema": {"$ref": "#/$defs/section_schema"},
        "skills_item_schema": {"$ref": "#/$defs/section_schema"},
        "abilities_item_schema": {"$ref": "#/$defs/section_schema"},
        "spells_item_schema": {"$ref": "#/$defs/section_schema"},
        "inventory_item_schema": {"$ref": "#/$defs/section_schema"},
        "custom_fields": {"$ref": "#/$defs/section_schema"}
    },
    "additionalProperties": False,  # não permite seções extras não listadas
    "$defs": {
        "section_schema": {
            "type": "object",
            "properties": {
                "default": {"type": "boolean"},
                "added_fields": {"type": "object"},
                "field_overrides": {"type": "object"},
                "custom_schema": {"type": "object"}
            },
            "additionalProperties": False,
            "default": {},  # se omitido, assume dicionário vazio
            "if": {
                "properties": {"default": {"const": False}},
                "required": ["default"]
            },
            "then": {
                # exige custom_schema quando default=false
                "required": ["custom_schema"]
            }
        }
    }
}
