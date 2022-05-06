from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.exceptions import ErrorDetail
from rest_framework.authtoken.models import Token
from app.models import User


class UserAuthTestCase(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('user_login')
        self.request_data = {
            'email': 'test@test.com',
            'password': 'password',
        }
        self.user = User.objects.create(email='test@test.com')
        self.user.set_password(self.request_data['password'])
        self.user.save()
        Token.objects.get_or_create(user=self.user)

    def test_all_fields_are_blank(self):
        request_data = {
            'email': '',
            'password': '',
        }

        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'],
                         [ErrorDetail(string='This field may not be blank.', code='blank')])
        self.assertEqual(response.data['password'],
                         [ErrorDetail(string='This field may not be blank.', code='blank')])
        self.assertEqual(set(response.data.keys()), set(request_data.keys()))

    def test_email_field_is_blank(self):
        self.request_data['email'] = ''
        expected_errors_keys = {'email'}

        response = self.client.post(self.url, self.request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'],
                         [ErrorDetail(string='This field may not be blank.', code='blank')])
        self.assertEqual(set(response.data.keys()), expected_errors_keys)

    def test_email_is_required(self):
        request_data = {
            'password': 'password',
        }
        expected_errors_keys = {'email'}

        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'],
                         [ErrorDetail(string='This field is required.', code='required')])
        self.assertEqual(set(response.data.keys()), expected_errors_keys)

    def test_email_field_are_incorrectly_filled(self):
        self.request_data['email'] = 'this is my email'
        expected_error_key = {'email'}

        response = self.client.post(self.url, self.request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response.data.keys()), set(expected_error_key))
        self.assertEqual(response.data['email'],
                         [ErrorDetail(string='Enter a valid email address.', code='invalid')]
                         )

    def test_password_is_required(self):
        request_data = {
            'email': 'test@test.com',
        }
        expected_errors_keys = {'password'}

        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password'],
                         [ErrorDetail(string='This field is required.', code='required')])
        self.assertEqual(set(response.data.keys()), expected_errors_keys)

    def test_password_field_is_blank(self):
        self.request_data['password'] = ''
        expected_errors_keys = {'password'}

        response = self.client.post(self.url, self.request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password'],
                         [ErrorDetail(string='This field may not be blank.', code='blank')])
        self.assertEqual(set(response.data.keys()), expected_errors_keys)

    def test_user_auth_successful(self):
        expected_success_keys = {'success', 'access_token'}

        response = self.client.post(self.url, self.request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], "You have successfully logged in !")
        self.assertEqual(set(response.data.keys()), expected_success_keys)

    def test_user_logout_without_authenticate(self):
        self.url = reverse('user_logout')
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_logout_successful(self):
        self.client.force_authenticate(user=self.user)
        self.url = reverse('user_logout')
        expected_success_keys = {'success'}

        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], "You have successfully logged out !")
        self.assertEqual(set(response.data.keys()), expected_success_keys)
