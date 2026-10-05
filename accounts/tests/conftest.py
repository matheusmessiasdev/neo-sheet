import pytest
from rest_framework.test import APIClient
from accounts.tests.factories import UserFactory
from django.test import override_settings


@pytest.fixture(autouse=True)
def use_test_urlconf():
    with override_settings(ROOT_URLCONF='proto_sheet.urls'):
        yield


@pytest.fixture
def api_client():
    """Basic API Client for non authenticated tests."""
    return APIClient()


@pytest.fixture
def user():
    """Returns a user created by UserFactory."""
    return UserFactory()


@pytest.fixture
def authenticated_client(api_client, user):
    """Authenticated Client by a created user."""
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.fixture
def auth_token(user):
    """Returns a JWT Token for the user."""
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }


@pytest.fixture
def api_client_with_token(api_client, auth_token):
    """Client with a JWT token in the Authorization header."""
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {auth_token["access"]}')
    return api_client
