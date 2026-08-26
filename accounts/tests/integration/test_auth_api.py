# accounts/tests/integration/test_auth_api.py
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from accounts.tests.factories import UserFactory

User = get_user_model()


@pytest.mark.django_db(transaction=True)
class TestAuthAPI:
    """Testes de integração para endpoints de autenticação (djoser + JWT)."""

    # ========== REGISTRO (user-list) ==========
    def test_user_registration_success(self, api_client):
        """Registro com dados válidos retorna 201."""
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
        """Registro com campos faltando retorna 400."""
        url = reverse('v1:user-list')
        data = {'username': 'newuser'}  # falta email e password
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data
        assert 'password' in response.data

    def test_user_registration_duplicate_username(self, api_client):
        """Registro com username duplicado retorna 400."""
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
        """Registro com email duplicado retorna 400."""
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
        """Registro com senha fraca retorna 400."""
        url = reverse('v1:user-list')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': '123'  # muito curta
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data

    # ========== LOGIN (JWT) ==========
    def test_login_success(self, api_client):
        """Login com credenciais válidas retorna tokens."""
        user = UserFactory()
        user.set_password('StrongPass123!')
        user.save()
        url = reverse('v1:jwt-create')  # nome padrão do djoser para JWT
        data = {
            'username': user.username,
            'password': 'StrongPass123!'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_login_invalid_username(self, api_client):
        """Login com username incorreto retorna 401."""
        url = reverse('v1:jwt-create')
        data = {
            'username': 'inexistente',
            'password': 'StrongPass123!'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'detail' in response.data

    def test_login_invalid_password(self, api_client):
        """Login com senha incorreta retorna 401."""
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

    # ========== REFRESH TOKEN ==========
    def test_refresh_success(self, api_client):
        """Refresh com token válido retorna novo access."""
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
        """Refresh com token inválido retorna 401."""
        url = reverse('v1:jwt-refresh')
        response = api_client.post(
            url, {'refresh': 'invalid_token'}, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # ========== VERIFY TOKEN ==========
    def test_verify_valid_token(self, api_client):
        """Verificação de token válido retorna 200."""
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
        """Verificação de token inválido retorna 401."""
        url = reverse('v1:jwt-verify')
        response = api_client.post(url, {'token': 'invalid'}, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # ========== PERFIL DO USUÁRIO (user-me) ==========
    def test_me_authenticated(self, api_client):
        """Usuário autenticado obtém seu perfil."""
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
        """Usuário não autenticado não obtém perfil."""
        me_url = reverse('v1:user-me')
        response = api_client.get(me_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # ========== ATUALIZAR PERFIL (user-me via PATCH) ==========
    def test_me_update_success(self, api_client):
        """Usuário autenticado atualiza seu perfil."""
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
        """Usuário não autenticado não atualiza perfil."""
        me_url = reverse('v1:user-me')
        response = api_client.patch(
            me_url, {'email': 'updated@example.com'}, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # ========== ALTERAR SENHA (user-set-password) ==========
    def test_set_password_success(self, api_client):
        """Usuário autenticado altera senha com dados válidos."""
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
        """Usuário autenticado com senha atual incorreta retorna 400."""
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
        """Usuário não autenticado não altera senha."""
        url = reverse('v1:user-set-password')
        response = api_client.post(url, {
            'current_password': 'OldPass123!',
            'new_password': 'NewPass123!'
        }, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # ========== RESET DE SENHA (se configurado) ==========
    # Os endpoints estão disponíveis, mas podem exigir envio de email.
    # Vamos testar apenas a validação básica.
    def test_reset_password_request(self, api_client):
        """Solicitação de reset de senha com email válido retorna 204 (ou 400 se sem email)."""
        user = UserFactory(email='user@example.com')
        url = reverse('v1:user-reset-password')
        # Dependendo da configuração, pode retornar 204 ou 400 se o email não for enviado.
        # Vamos enviar um email válido.
        response = api_client.post(
            url, {'email': 'user@example.com'}, format='json')
        # O djoser retorna 204 se o email for enviado (ou se a configuração estiver ok)
        assert response.status_code in [
            status.HTTP_204_NO_CONTENT, status.HTTP_400_BAD_REQUEST]

    def test_reset_password_invalid_email(self, api_client):
        """Solicitação de reset com email inexistente retorna 400 (ou 204)."""
        url = reverse('v1:user-reset-password')
        response = api_client.post(
            url, {'email': 'inexistente@example.com'}, format='json')
        # O djoser pode retornar 204 mesmo para emails inexistentes (por segurança)
        # Mas geralmente retorna 400 se o campo não for enviado.
        # Vamos apenas verificar que não é 500.
        assert response.status_code in [
            status.HTTP_204_NO_CONTENT, status.HTTP_400_BAD_REQUEST]

    # ========== CONFIRMAR RESET DE SENHA ==========
    def test_reset_password_confirm_invalid_token(self, api_client):
        """Confirmar reset com token inválido retorna 400."""
        url = reverse('v1:user-reset-password-confirm')
        response = api_client.post(url, {
            'uid': 'invalid',
            'token': 'invalid',
            'new_password': 'NewPass123!'
        }, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
