from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from app.models import User


class UserAuthTestCase(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('user_login')
        self.request_data = {
            'email': 'test@test.com',
            'password': 'password',
        }
        self.user = User.objects.create(email='test@test.com', language='de')
        self.user.set_password(self.request_data['password'])
        self.user.save()
        Token.objects.get_or_create(user=self.user)

    def test_user_auth_successful(self):
        expected_success_keys = {'success', 'access_token'}

        response = self.client.post(self.url, self.request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], "Sie haben sich erfolgreich angemeldet!")
        self.assertEqual(set(response.data.keys()), expected_success_keys)

    def test_user_logout_successful(self):
        self.client.force_authenticate(user=self.user)
        self.url = reverse('user_logout')
        expected_success_keys = {'success'}

        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], "You have successfully logged out !")
        self.assertEqual(set(response.data.keys()), expected_success_keys)
