import factory
from django.contrib.auth import get_user_model
from sheets.models import ProfileModel
User = get_user_model()


class ProfileFactory(factory.django.DjangoModelFactory):
    system_id = factory.Sequence(lambda n: f'system_{n}')
    user = factory.SubFactory(
        'accounts.tests.factories.UserFactory')
    display_name = factory.LazyAttribute(
        lambda obj: f'Display for {obj.system_id}')
    schemas = dict()
    custom_fields = dict()
    is_official = False

    class Meta:
        model = ProfileModel
