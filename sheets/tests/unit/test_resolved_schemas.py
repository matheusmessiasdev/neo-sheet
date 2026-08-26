import pytest
from copy import deepcopy
from sheets.services.resolved_schemas import resolve_schemas
from sheets.services.profile_template import PROFILE_BLANK_SCHEMA


class TestResolveSchemas:
    def test_resolve_schemas_empty(self):
        """
        Base case: no modifications, returns the template with empty _meta.
        """
        result = resolve_schemas({})
        expected_schemas = deepcopy(PROFILE_BLANK_SCHEMA['schemas'])
        expected_schemas['_meta'] = {'added_schemas': {}}
        assert expected_schemas == result

    def test_resolve_schemas_with_added_fields(self):
        """Add fields to an existing section."""
        modifications = {
            'identity_schema': {
                'added_fields': {'title': ''}
            }
        }
        result = resolve_schemas(modifications)

        assert result['identity_schema']['added_fields']['title'] == ''
        assert '_meta' in result
        assert 'identity_schema' in result['_meta']['added_schemas']

    def test_resolve_schemas_with_field_overrides(self):
        """Overrides a field for a object."""
        modifications = {
            'identity_schema': {
                'field_overrides': {'level': {'label': 'Rank'}}
            }
        }
        result = resolve_schemas(modifications)

        assert result['identity_schema']['field_overrides']['level'] == {
            'label': 'Rank'}
        assert '_meta' in result

    def test_resolve_schemas_with_custom_schema(self):
        """Substitutes a section completely with custom_schema (default: False)."""
        modifications = {
            'attributes_schema': {
                'default': False,
                'custom_schema': {'forca': 0, 'destreza': 0}
            }
        }
        result = resolve_schemas(modifications)
        # A seção attributes_schema deve conter apenas o custom_schema

        print(f'Result: {result}')

        assert result['attributes_schema']['custom_schema'] == {
            'forca': 0, 'destreza': 0}
        assert '_meta' in result
        assert 'attributes_schema' in result['_meta']['added_schemas']

    def test_resolve_schemas_combined(self):
        """Combination of multiple modifications."""
        modifications = {
            'identity_schema': {'added_fields': {'title': ''}},
            'status_schema': {'field_overrides': {'health': {'max': 200}}},
            'inventory_item_schema': {'added_fields': {'quantity': 1}}
        }
        result = resolve_schemas(modifications)
        print(result)
        assert result['identity_schema']['added_fields']['title'] == ''
        assert result['status_schema']['field_overrides']['health'] == {
            'max': 200}
        assert result['inventory_item_schema']['added_fields']['quantity'] == 1
        assert set(result['_meta']['added_schemas'].keys()) == {
            'identity_schema', 'status_schema', 'inventory_item_schema'}
