from django.urls import reverse
from django.core import mail
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase, override_settings
from app.models import User


class UserPasswordChangeTestCase(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('user_change_password')
        self.request_data = {
            "current_password": "password",
            "new_password": "new_password",
            "confirm_new_password": "new_password"
        }
        self.user = User.objects.create(email='test@test.com', language='de')
        self.user.set_password(self.request_data['current_password'])
        self.user.save()
        self.client.cookies.load({'django_language': self.user.language})

    def test_user_can_not_change_password_without_current_password_field(self):
        self.client.force_authenticate(user=self.user)
        self.request_data['current_password'] = ''
        expected_error_key = {'current_password'}

        response = self.client.patch(self.url, self.request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response.data.keys()), expected_error_key)
        self.assertEqual(response.data['current_password'],
                         [ErrorDetail(string='Dieses Feld darf nicht leer sein.', code='blank')])

    def test_user_can_not_change_password_without_new_password_field(self):
        self.client.force_authenticate(user=self.user)
        self.request_data['new_password'] = ''
        expected_error_key = {'new_password'}

        response = self.client.patch(self.url, self.request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response.data.keys()), expected_error_key)
        self.assertEqual(response.data['new_password'],
                         [ErrorDetail(string='Dieses Feld darf nicht leer sein.', code='blank')])

    def test_user_can_not_change_password_without_confirm_new_password_field(self):
        self.client.force_authenticate(user=self.user)
        self.request_data['confirm_new_password'] = ''
        expected_error_key = {'confirm_new_password'}

        response = self.client.patch(self.url, self.request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response.data.keys()), expected_error_key)
        self.assertEqual(response.data['confirm_new_password'],
                         [ErrorDetail(string='Dieses Feld darf nicht leer sein.', code='blank')])

    def test_user_can_not_change_password_with_not_matched_new_passwords(self):
        self.client.force_authenticate(user=self.user)
        self.request_data['new_password'] = 'not_matched_password'
        expected_error_key = {'new_password'}

        response = self.client.patch(self.url, self.request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response.data.keys()), expected_error_key)
        self.assertEqual(response.data['new_password'],
                         [ErrorDetail(string='Diese Passwörter stimmen nicht überein', code='invalid')])

    def test_user_can_not_change_password_with_same_current_and_new_passwords(self):
        self.client.force_authenticate(user=self.user)
        self.request_data = {
            'current_password': 'password',
            'new_password': 'password',
            'confirm_new_password': 'password'
        }
        expected_error_key = {'new_password'}

        response = self.client.patch(self.url, self.request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response.data.keys()), expected_error_key)
        self.assertEqual(response.data['new_password'],
                         [ErrorDetail(string='Die Passwörter müssen nicht identisch sein.', code='invalid')])

    @override_settings(task_eager_propagates=True, task_always_eager=True, broker_url='memory://', backend='memory')
    def test_user_can_change_password(self):
        self.client.force_authenticate(user=self.user)
        expected_success_key = {'success'}

        response = self.client.patch(self.url, self.request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.data.keys()), expected_success_key)
        self.assertEqual(response.data['success'], 'Sie haben sich erfolgreich angemeldet!')
        self.assertEqual(mail.outbox[0].subject, 'Das Passwort wurde geändert!!!')
        self.assertEqual(mail.outbox[0].to, [self.user.email])
