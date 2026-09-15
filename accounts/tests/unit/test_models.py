import pytest
# accounts/tests/unit/test_models.py
from django.contrib.auth import get_user_model
from accounts.tests.factories import UserFactory

User = get_user_model()


@pytest.mark.django_db(transaction=True)
class TestUserModel:
    def test_user_creation(self):
        """Test basic user creation with factory."""
        user = UserFactory()
        assert user.pk is not None
        assert user.username is not None
        assert user.email is not None

    def test_user_str_method(self):
        """Test the __str__ method. """
        user = UserFactory(username='testuser')
        # Se você sobrescreveu __str__, ajuste a expectativa
        # Exemplo: se __str__ retorna username
        assert str(user) == 'testuser'
        # Ou se retorna email
        # assert str(user) == user.email
