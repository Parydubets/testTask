from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User

class TokenObtainPairTests(APITestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username="TestUser",
            first_name="test",
            last_name="user",
            email="test@gmail.com",
            password="somepas2"
        )
        self.token_url = reverse('token_obtain_pair')

    def test_with_valid_credentials(self):
        """
        Ensure a token is obtained successfully with valid credentials.
        """
        data = {
            'username': 'TestUser',
            'password': 'somepas2'
        }
        response = self.client.post(self.token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_with_invalid_credentials(self):
        """
        Ensure a token is not obtained with invalid credentials.
        """
        data = {
            'username': 'TestUser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)
        self.assertEqual(response.data['detail'], 'No active account found with the given credentials')
