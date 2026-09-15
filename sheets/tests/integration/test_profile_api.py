import pytest
from rest_framework import status
from django.urls import reverse
from sheets.models import ProfileModel
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from sheets.tests.factories import ProfileFactory


@pytest.mark.django_db(transaction=True)
class TestProfileAPI:

    def test_list_anonymous_views_official_only(self, api_client):
        official_1 = ProfileFactory(
            user=None, is_official=True, system_id='official1')
        official_2 = ProfileFactory(
            user=None, is_official=True, system_id='official2')

        User = get_user_model()
        user = User.objects.create_user(
            username='testuser', password='TestPass123#')
        private = ProfileFactory(
            user=user, is_official=False, system_id='private_testuser')

        url = reverse('v1:profile-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        response_system_ids = {p['system_id'] for p in response.data}

        assert official_1.system_id in response_system_ids
        assert official_2.system_id in response_system_ids
        assert private.system_id not in response_system_ids

    def test_list_authenticated_views_official_and_own(self, authenticated_client, official_profile):
        """Authenticated user see official profiles + their own profiles."""
        client, user = authenticated_client
        private_profile = ProfileModel.objects.create(
            user=user,
            system_id='private_system',
            display_name='Private System'
        )
        url = reverse('v1:profile-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        system_ids = [p['system_id'] for p in response.data]
        assert official_profile.system_id in system_ids
        assert private_profile.system_id in system_ids
        other_user = get_user_model().objects.create_user(username='other')
        other_profile = ProfileModel.objects.create(
            user=other_user,
            system_id='other_system',
            display_name='Other System'
        )
        response = client.get(url)
        assert 'other_system' not in [p['system_id'] for p in response.data]

    def test_create_profile_authenticated(self, authenticated_client):
        """Authenticated user creates profile with auto association."""
        client, user = authenticated_client
        url = reverse('v1:profile-list')
        data = {
            'system_id': 'new_system',
            'display_name': 'New System',
            'schemas': {}
        }
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        profile = ProfileModel.objects.get(system_id='new_system')
        assert profile.user == user

    def test_create_official_profile_as_non_admin(self, authenticated_client):
        """Non-admin user cannot create an official profile."""
        client, user = authenticated_client
        url = reverse('v1:profile-list')
        data = {
            'system_id': 'official_system',
            'display_name': 'Official System',
            'is_official': True,
            'schemas': {}
        }
        response = client.post(url, data, format='json')
        assert response.status_code in [
            status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST]

    def test_retrieve_private_profile_only_owner(self, authenticated_client):
        """
        Private profile: only the owner can see.
        """
        User = get_user_model()
        owner = User.objects.create_user(username='owner', password='pass')
        private_profile = ProfileFactory(
            user=owner,
            is_official=False,
            system_id='private_owner'
        )
        url = reverse('v1:profile-detail',
                      kwargs={'system_id': private_profile.system_id})

        anon_client = APIClient()
        response = anon_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        other_user = User.objects.create_user(
            username='other', password='pass')
        other_client = APIClient()
        other_client.force_authenticate(user=other_user)
        response = other_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        owner_client = APIClient()
        owner_client.force_authenticate(user=owner)
        response = owner_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['system_id'] == private_profile.system_id

    def test_update_private_profile_owner_only(self, authenticated_client, user_profile):
        """Only the owner can update a private profile."""
        client, user, profile = user_profile
        url = reverse('v1:profile-detail',
                      kwargs={'system_id': profile.system_id})
        data = {'display_name': 'Updated Name'}
        response = client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        profile.refresh_from_db()
        assert profile.display_name == 'Updated Name'
        other_client = APIClient()
        other_user = get_user_model().objects.create_user(username='other')
        other_client.force_authenticate(user=other_user)
        response = other_client.patch(
            url, {'display_name': 'Hacked'}, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_private_profile_owner_only(self, authenticated_client, user_profile):
        """Only the owner can delete a private profile."""
        client, user, profile = user_profile
        url = reverse('v1:profile-detail',
                      kwargs={'system_id': profile.system_id})
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not ProfileModel.objects.filter(id=profile.id).exists()
        response = client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_official_profile_anyone(self, api_client, authenticated_client, official_profile):
        """Official profile is visible to everyone."""
        url = reverse('v1:profile-detail',
                      kwargs={'system_id': official_profile.system_id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['system_id'] == official_profile.system_id
        client, user = authenticated_client
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
