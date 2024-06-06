from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from app.models import User
from rest_framework.views import APIView
from rest_framework import permissions

def test_with_client(client):
    response = client.get('/home')
    assert response.content ==  b'{"message":"Hello, World!"}'

class AccountTests(APITestCase):

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """

        url = reverse('user-create')
        data = {
                    "username": "TestUser",
                    "first_name": "test",
                    "last_name": "user",
                    "email": "test@gmail.com",
                    "password": "somepas2"
                }
        initial_user_number = User.objects.count()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count() - initial_user_number, 1)
        self.assertEqual(User.objects.get(username= "TestUser").username, 'TestUser')


class AccountTestsAdmin(APITestCase):
    def setUp(self):
        self.url_update = reverse('user-update', args=[2])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_token()}')


    def get_token(self):
        """
        Log in admin user
        """
        data = {
            'username': 'admin',
            'password': 'adminhere1'
        }
        response = self.client.post(reverse('token_obtain_pair'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        return  response.data['access']


    def test_availability(self):

        response = self.client.get('/api/top_votes')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_successfully(self):
        """
        Ensure we can successfully update an existing user.
        """
        data = {
            "first_name": "updatedfirst",
            "last_name": "updatedlast",
            "email": "updatedtest@gmail.com",
        }
        print(self.url_update, data)
        response = self.client.put(self.url_update, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_user = User.objects.get(username="TestUser")
        self.assertEqual(updated_user.first_name, 'updatedfirst')
        self.assertEqual(updated_user.last_name, 'updatedlast')
        self.assertEqual(updated_user.email, 'updatedtest@gmail.com')

    def test_update_user_without_permission(self):
        other_user = User.objects.create_user(
            username="OtherUser",
            first_name="other",
            last_name="user",
            email="other@gmail.com",
            password="otherpass"
        )
        data = {
            "first_name": "updatedfirst",
            "last_name": "updatedlast",
            "email": "updatedtest@gmail.com",
        }
        response = self.client.put(self.url_update, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_non_existent_user(self):
        """
        Ensure we get a 404 error when trying to update a non-existent user.
        """
        non_existent_url = reverse('user-update', args=[9999])
        data = {
            "first_name": "updatedfirst",
            "last_name": "updatedlast",
            "email": "updatedtest@gmail.com",
        }
        response = self.client.put(non_existent_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401)

    def test_update_user_without_authentication(self):
        """
        Ensure an unauthenticated user cannot update a user's details.
        """
        data = {
            "first_name": "updatedfirst",
            "last_name": "updatedlast",
            "email": "updatedtest@gmail.com",
        }
        response = self.client.put(self.url_update, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)