BASE_SCHEMA_FIELDS = [
    "identity",
    "attributes",
    "skills",
    "status",
    "inventory",
    "spells",
    "defense",
    "abilities",
    "stacks",
    "corruption",
    "advantages_disadvantages",
]

BASE_SCHEMA_DEFAULTS = {
    "identity": {
        "name": '',
        "level": 0,
        "experience": 0,
        "species": '',
        "role": '',
    },
    "attributes": {},
    "status": {},
    "defense": {},
    "skills": [],
    "abilities": [],
    "spells": [],
    "inventory": [],
    "stacks": None,
    "advantages_disadvantages": None,
    "custom_fields": {},
}


def base_schema():
    return BASE_SCHEMA_DEFAULTS
