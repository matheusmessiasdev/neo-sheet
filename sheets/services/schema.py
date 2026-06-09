BASE_SCHEMA_FIELDS = [
    "identity",
    "attributes",
    "status",
    "defense",
    "skills",
    "abilities",
    "spells",
    "inventory",
    "custom",
]


BASE_IDENTITY_SCHEMA = {
    "name": '',
    "level": 0,
    "experience": 0,
    "species": '',
    "role": '',
}
BASE_ATTRIBUTES_SCHEMA = {
    "strength": {"value": 0, "modifier": 0},
    "dexterity": {"value": 0, "modifier": 0},
    "intelligence": {"value": 0, "modifier": 0},
    "constitution": {"value": 0, "modifier": 0},
    "wisdom": {"value": 0, "modifier": 0},

}
BASE_STATUS_SCHEMA = {
    "health": {"current": 0, "max": 9999},
    "sanity": {"current": 0, "max": 9999},
    "mana": {"current": 0, "max": 9999},

}


BASE_DEFENSE_SCHEMA = {
    "base_ac": 10,
    "protection_value": 0,
    "bonus": 0,
    "total": 0,
    "resistances": "",
    "imunities": "",
}

BASE_SKILLS_SCHEMA = {
    "name": "",
    "attribute": "",
    "proficiency_bonus": 0,
    "extra": 0,
    "total": 0,
}

BASE_ABILITIES_SCHEMA = {
    "name": "",
    "cost": 0,
    "type": "",
    "description": "",
}

BASE_SPELLS_SCHEMA = {
    "name": "",
    "cost": 0,
    "casting_time": "",
    "range_area": "",
    "duration": "",
    "element": "",
    "type": "",
    "description": "",
}

BASE_INVENTORY_SCHEMA = {
    "name": "",
    "weight": 0,
    "amount": 0,
    "description": "",
}

BASE_SCHEMA_DEFAULTS = {
    "identity": BASE_IDENTITY_SCHEMA,
    "attributes": BASE_ATTRIBUTES_SCHEMA,
    "status": BASE_STATUS_SCHEMA,
    "defense": BASE_DEFENSE_SCHEMA,
    "skills": [BASE_SKILLS_SCHEMA],
    "abilities": [BASE_ABILITIES_SCHEMA],
    "spells": [BASE_SPELLS_SCHEMA],
    "inventory": [BASE_INVENTORY_SCHEMA],
    "custom": {},
}


def base_schema():
    return BASE_SCHEMA_DEFAULTS
