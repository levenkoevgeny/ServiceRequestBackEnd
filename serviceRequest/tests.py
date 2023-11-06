from rest_framework.test import APITestCase
from rest_framework import status
from .models import Location


class CustomUserTests(APITestCase):
    def setUp(self):
        self.userData = {"username": "testUser", "password": "12345678", "is_active": True, "is_superuser": True,
                         "is_staff": True}
        self.client.post('/api/users/', self.userData, format="json")
        response = self.client.post('/api/token/', self.userData, format="json")
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def test_user_can_not_get_data_without_admin_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'wrong_credentials')
        response = self.client.get('/api/locations/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_location(self):
        response = self.client.post('/api/locations/', {"location": "Location 1"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_locations(self):
        self.client.post('/api/locations/', {"location": "Location 1"}, format="json")
        self.client.post('/api/locations/', {"location": "Location 2"}, format="json")
        self.client.post('/api/locations/', {"location": "Location 3"}, format="json")
        response = self.client.get('/api/locations/?location__icontains=Location 1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_update_location(self):
        self.client.post('/api/locations/', {"location": "Location 1"}, format="json")
        location = Location.objects.get(location="Location 1")
        response = self.client.put('/api/locations/' + str(location.id) + '/', {"location": "Updated location"},
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_location(self):
        self.client.post('/api/locations/', {"location": "Location 1"}, format="json")
        location = Location.objects.get(location="Location 1")
        response = self.client.delete('/api/locations/' + str(location.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
