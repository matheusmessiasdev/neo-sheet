import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from sheets.models import ProfileModel
from sheets.tests.factories import ProfileFactory
from accounts.tests.factories import UserFactory  # Ajuste conforme seu app

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.fixture
def official_profile():
    return ProfileFactory(user=None, is_official=True)


@pytest.fixture
def user_profile(authenticated_client):
    client, user = authenticated_client
    profile = ProfileFactory(user=user)
    return client, user, profile
