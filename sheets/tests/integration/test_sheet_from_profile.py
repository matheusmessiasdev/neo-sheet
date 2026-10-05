import pytest
from sheets.services.sheet_from_profile import configure_sheet_from_profile, strip_metadata
from sheets.tests.factories import ProfileFactory
from sheets.services.schema import BASE_SCHEMA_DEFAULTS
from copy import deepcopy


class TestStripMetadata:

    def test_strip_metadata_dict(self):
        """Remove dict keys that start with _."""
        data = {'_meta': 'ignore', 'name': 'test',
                'nested': {'_hidden': True, 'value': 1}}
        result = strip_metadata(data)
        assert '_meta' not in result
        assert 'name' in result
        assert '_hidden' not in result['nested']
        assert result['nested']['value'] == 1

    def test_strip_metadata_list(self):
        """Processes lists recursively."""
        data = [{'_id': 1, 'name': 'a'}, {'_id': 2, 'name': 'b'}]
        result = strip_metadata(data)
        for item in result:
            assert '_id' not in item
            assert 'name' in item

    def test_strip_metadata_scalar(self):
        """Simple values are returned without changes."""
        assert strip_metadata(10) == 10
        assert strip_metadata('test') == 'test'
        assert strip_metadata(None) is None


@pytest.mark.django_db(transaction=True)
class TestConfigureSheetFromProfile:

    @pytest.fixture
    def base_sheet(self):
        return deepcopy(BASE_SCHEMA_DEFAULTS)

    def test_no_modifications(self):
        """Profiles without modification return base schema."""
        profile = ProfileFactory(schemas={})
        sheet = configure_sheet_from_profile(profile)
        expected = strip_metadata(deepcopy(BASE_SCHEMA_DEFAULTS))
        assert sheet == expected

    def test_with_added_fields(self):
        """Add fields to a section (identity)."""
        modifications = {
            'identity_schema': {
                'added_fields': {'title': ''}
            }
        }
        profile = ProfileFactory(schemas=modifications)
        sheet = configure_sheet_from_profile(profile)
        assert sheet['identity']['title'] == ''

    def test_with_field_overrides_substitution(self):
        """Overrides a field (level) completely for an object."""
        modifications = {
            'identity_schema': {
                'field_overrides': {'level': {'label': 'Rank'}}
            }
        }
        profile = ProfileFactory(schemas=modifications)
        sheet = configure_sheet_from_profile(profile)
        assert sheet['identity']['level'] == {'label': 'Rank'}

    def test_with_custom_schema_for_dict(self):
        """Overrides completely a section by custom_schema."""
        modifications = {
            'attributes_schema': {
                'default': False,
                'custom_schema': {'forca': 0, 'destreza': 0}
            }
        }
        profile = ProfileFactory(schemas=modifications)
        sheet = configure_sheet_from_profile(profile)
        assert sheet['attributes'] == {'forca': 0, 'destreza': 0}

    def test_with_custom_schema_for_list(self):
        """Overrides completely a section that is initially a list."""
        modifications = {
            'abilities_item_schema': {
                'default': False,
                'custom_schema': {'name': '', 'cooldown': 0}
            }
        }
        profile = ProfileFactory(schemas=modifications)
        sheet = configure_sheet_from_profile(profile)
        assert isinstance(sheet['abilities'], list)
        assert sheet['abilities'][0] == {'name': '', 'cooldown': 0}

    def test_added_fields_to_list_item(self):
        """Add field to an item list (inventory)."""
        modifications = {
            'inventory_item_schema': {
                'added_fields': {'quantity': 1}
            }
        }
        profile = ProfileFactory(schemas=modifications)
        sheet = configure_sheet_from_profile(profile)
        for item in sheet['inventory']:
            assert 'quantity' in item
            assert item['quantity'] == 1

    def test_field_overrides_with_null_removes_field(self):
        """field_overrides with None removes the field from base."""
        modifications = {
            'identity_schema': {
                'field_overrides': {'experience': None}
            }
        }
        profile = ProfileFactory(schemas=modifications)
        sheet = configure_sheet_from_profile(profile)
        assert 'experience' not in sheet['identity']

    def test_metadata_removal_at_all_levels(self):
        """Metadata (_*) are removed across all levels."""
        modifications = {
            'identity_schema': {
                'added_fields': {
                    'title': '',
                    '_version': '1.0'
                },
                'field_overrides': {
                    'level': {'_label': 'Rank', 'value': 1}
                }
            }
        }
        profile = ProfileFactory(schemas=modifications)
        sheet = configure_sheet_from_profile(profile)
        assert '_version' not in sheet['identity']
        assert '_label' not in sheet['identity']['level']
        assert sheet['identity']['level']['value'] == 1
