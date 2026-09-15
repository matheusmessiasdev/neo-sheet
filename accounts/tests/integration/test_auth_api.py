import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from accounts.tests.factories import UserFactory

User = get_user_model()


@pytest.mark.django_db(transaction=True)
class TestAuthAPI:
    """Integration tests for authentication endpoints (djoser + JWT)."""

    def test_user_registration_success(self, api_client):
        """Registration with valid data returns 201."""
        url = reverse('v1:user-list')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'StrongPass123!'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.data
        assert response.data['username'] == 'newuser'
        assert response.data['email'] == 'new@example.com'
        assert 'password' not in response.data

    def test_user_registration_missing_fields(self, api_client):
        """Registration with valid data returns 201."""
        url = reverse('v1:user-list')

        data = {'username': 'newuser'}

        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data
        assert 'password' in response.data

    def test_user_registration_duplicate_username(self, api_client):
        """Registration with duplicate username returns 400."""
        existing_user = UserFactory(username='existing')
        url = reverse('v1:user-list')
        data = {
            'username': 'existing',
            'email': 'new@example.com',
            'password': 'StrongPass123!'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'username' in response.data

    def test_user_registration_duplicate_email(self, api_client):
        """Registration with duplicate username returns 400."""
        existing_user = UserFactory(email='existing@example.com')
        url = reverse('v1:user-list')
        data = {
            'username': 'newuser',
            'email': 'existing@example.com',
            'password': 'StrongPass123!'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_user_registration_weak_password(self, api_client):
        """Registration with weak password returns 400."""
        url = reverse('v1:user-list')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': '123'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data

    def test_login_success(self, api_client):
        """Login with valid credentials returns tokens."""
        user = UserFactory()
        user.set_password('StrongPass123!')
        user.save()
        url = reverse('v1:jwt-create')
        data = {
            'username': user.username,
            'password': 'StrongPass123!'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_login_invalid_username(self, api_client):
        """Login with incorrect username returns 401."""
        url = reverse('v1:jwt-create')
        data = {
            'username': 'inexistente',
            'password': 'StrongPass123!'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'detail' in response.data

    def test_login_invalid_password(self, api_client):
        """Login with incorrect password returns 401.."""
        user = UserFactory(username='testuser')
        user.set_password('StrongPass123!')
        user.save()
        url = reverse('v1:jwt-create')
        data = {
            'username': 'testuser',
            'password': 'WrongPass123!'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_success(self, api_client):
        """Refresh with valid token returns new access token."""
        user = UserFactory()
        login_url = reverse('v1:jwt-create')
        data = {'username': user.username, 'password': 'Test@1234'}
        login_response = api_client.post(login_url, data, format='json')
        refresh_token = login_response.data['refresh']

        refresh_url = reverse('v1:jwt-refresh')
        response = api_client.post(
            refresh_url, {'refresh': refresh_token}, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data

    def test_refresh_invalid_token(self, api_client):
        """Refresh with invalid token returns 401."""
        url = reverse('v1:jwt-refresh')
        response = api_client.post(
            url, {'refresh': 'invalid_token'}, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_verify_valid_token(self, api_client):
        """Verification of valid token returns 200."""
        user = UserFactory()
        login_url = reverse('v1:jwt-create')
        data = {'username': user.username, 'password': 'Test@1234'}
        login_response = api_client.post(login_url, data, format='json')
        access_token = login_response.data['access']

        verify_url = reverse('v1:jwt-verify')
        response = api_client.post(
            verify_url, {'token': access_token}, format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_verify_invalid_token(self, api_client):
        """Verification of invalid token returns 401."""
        url = reverse('v1:jwt-verify')
        response = api_client.post(url, {'token': 'invalid'}, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_me_authenticated(self, api_client):
        """Authenticated user retrieves their profile."""
        user = UserFactory()
        login_url = reverse('v1:jwt-create')
        data = {'username': user.username, 'password': 'Test@1234'}
        login_response = api_client.post(login_url, data, format='json')
        access_token = login_response.data['access']

        me_url = reverse('v1:user-me')
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = api_client.get(me_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == user.id
        assert response.data['username'] == user.username

    def test_me_unauthenticated(self, api_client):
        """Unauthenticated user cannot retrieve profile."""
        me_url = reverse('v1:user-me')
        response = api_client.get(me_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_me_update_success(self, api_client):
        """Authenticated user updates their profile."""
        user = UserFactory()
        login_url = reverse('v1:jwt-create')
        data = {'username': user.username, 'password': 'Test@1234'}
        login_response = api_client.post(login_url, data, format='json')
        access_token = login_response.data['access']

        me_url = reverse('v1:user-me')
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = api_client.patch(
            me_url, {'email': 'updated@example.com'}, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == 'updated@example.com'
        user.refresh_from_db()
        assert user.email == 'updated@example.com'

    def test_me_update_unauthenticated(self, api_client):
        """Unauthenticated user cannot update profile."""
        me_url = reverse('v1:user-me')
        response = api_client.patch(
            me_url, {'email': 'updated@example.com'}, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_set_password_success(self, api_client):
        """Authenticated user changes password with valid data."""
        user = UserFactory()
        user.set_password('OldPass123!')
        user.save()
        login_url = reverse('v1:jwt-create')
        data = {'username': user.username, 'password': 'OldPass123!'}
        login_response = api_client.post(login_url, data, format='json')
        access_token = login_response.data['access']

        url = reverse('v1:user-set-password')
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = api_client.post(url, {
            'current_password': 'OldPass123!',
            'new_password': 'NewPass123!'
        }, format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_set_password_invalid_current(self, api_client):
        """Authenticated user with incorrect current password returns 400."""
        user = UserFactory()
        user.set_password('OldPass123!')
        user.save()
        login_url = reverse('v1:jwt-create')
        data = {'username': user.username, 'password': 'OldPass123!'}
        login_response = api_client.post(login_url, data, format='json')
        access_token = login_response.data['access']

        url = reverse('v1:user-set-password')
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = api_client.post(url, {
            'current_password': 'WrongPass123!',
            'new_password': 'NewPass123!'
        }, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_set_password_unauthenticated(self, api_client):
        """Unauthenticated user cannot change password."""
        url = reverse('v1:user-set-password')
        response = api_client.post(url, {
            'current_password': 'OldPass123!',
            'new_password': 'NewPass123!'
        }, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_reset_password_request(self, api_client):
        """Password reset request with valid email returns 204 (or 400 if no email)."""
        user = UserFactory(email='user@example.com')
        url = reverse('v1:user-reset-password')
        response = api_client.post(
            url, {'email': 'user@example.com'}, format='json')
        assert response.status_code in [
            status.HTTP_204_NO_CONTENT, status.HTTP_400_BAD_REQUEST]

    def test_reset_password_invalid_email(self, api_client):
        """Password reset request with non-existent email returns 400 (or 204)."""
        url = reverse('v1:user-reset-password')
        response = api_client.post(
            url, {'email': 'inexistente@example.com'}, format='json')

        assert response.status_code in [
            status.HTTP_204_NO_CONTENT, status.HTTP_400_BAD_REQUEST]

    def test_reset_password_confirm_invalid_token(self, api_client):
        """Password reset confirmation with invalid token returns 400."""
        url = reverse('v1:user-reset-password-confirm')
        response = api_client.post(url, {
            'uid': 'invalid',
            'token': 'invalid',
            'new_password': 'NewPass123!'
        }, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
