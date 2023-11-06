from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser


class CustomUserTests(APITestCase):

    def setUp(self):
        self.userData = {"username": "testUser", "password": "12345678"}

    def test_api_create_user(self):
        response = self.client.post('/api/users/', self.userData, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_user_can_authenticate(self):
        self.client.post('/api/users/', self.userData, format="json")
        response = self.client.post('/api/token/', self.userData, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data, True)
        self.assertTrue('refresh' in response.data, True)
        response = self.client.post('/api/token/', {"username": "wrongTestUser", "password": "12345678"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
