import factory
from django.contrib.auth import get_user_model
from faker import Faker

fake = Faker()

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username',)
        # skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f'user_{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.django.Password('Test@1234')
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    is_active = True
    is_staff = False
    is_superuser = False
