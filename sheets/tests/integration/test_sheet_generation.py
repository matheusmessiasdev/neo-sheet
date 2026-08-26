import pytest
from rest_framework import status
from django.urls import reverse
from sheets.models import ProfileModel
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


@pytest.mark.django_db(transaction=True)
class TestSheetGeneration:

    def test_sheet_from_profile_authenticated(self, authenticated_client):
        """Usuário autenticado pode gerar ficha a partir de um perfil próprio."""
        client, user = authenticated_client
        profile = ProfileModel.objects.create(
            user=user,
            system_id='test_system',
            display_name='Test System',
            schemas={
                'identity_schema': {
                    'added_fields': {'title': ''}
                }
            }
        )
        url = reverse('v1:profile-sheet-from-profile',
                      kwargs={'system_id': profile.system_id})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        # A resposta deve conter a ficha gerada (sem metadados)
        sheet = response.data
        assert 'identity' in sheet
        assert 'title' in sheet['identity']
        # Verifica que metadados foram removidos (ex: _*)
        assert not any(key.startswith('_') for key in sheet['identity'].keys())

# TODO deixar tudo isolado com APIClient
    def test_sheet_from_profile_unauthorized(self, api_client, authenticated_client):
        """Usuário não pode gerar ficha de perfil que não possui."""
        User = get_user_model()
        client, user = authenticated_client
        # Cria perfil de outro usuário
        other_user = get_user_model().objects.create_user(username='other')
        other_profile = ProfileModel.objects.create(
            user=other_user,
            system_id='other_system',
            display_name='Other System'
        )
        url = reverse('v1:profile-sheet-from-profile',
                      kwargs={'system_id': other_profile.system_id})
        # Outro usuário tenta acessar
        other_user1 = User.objects.create_user(
            username='other1', password='pass')
        other_client = APIClient()
        other_client.force_authenticate(user=other_user1)
        response = other_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        # Anônimo também não
        anon_client = APIClient()
        response = anon_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_sheet_from_official_profile(self, api_client, official_profile):
        """Qualquer um pode gerar ficha a partir de um perfil oficial."""
        url = reverse('v1:profile-sheet-from-profile',
                      kwargs={'system_id': official_profile.system_id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'identity' in response.data
