from django.urls import reverse
from django.core import mail
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase, override_settings
from app.models import User


class UserPasswordChangeTestCase(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('user_switch_lang')
        self.request_data = {
            "language": "de"
        }
        self.user = User.objects.create(email='test@test.com', language='de')
        self.user.set_password('password')
        self.user.save()
        self.client.cookies.load({'django_language': self.user.language})

    def test_user_can_not_change_language_with_empty_field(self):
        self.client.force_authenticate(user=self.user)
        self.request_data['language'] = ''
        expected_error_key = {'language'}

        response = self.client.patch(self.url, self.request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response.data.keys()), expected_error_key)
        self.assertEqual(response.data['language'],
                         [ErrorDetail(string='Dieses Feld darf nicht leer sein.', code='blank')])

    def test_user_can_not_change_language_without_required_field(self):
        self.client.force_authenticate(user=self.user)
        self.request_data = {}
        expected_error_key = {'language'}

        response = self.client.patch(self.url, self.request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response.data.keys()), expected_error_key)
        self.assertEqual(response.data['language'],
                         [ErrorDetail(string='Dieses Feld ist erforderlich.', code='required')])

    def test_user_can_not_change_language_to_not_supported_language(self):
        self.client.force_authenticate(user=self.user)
        wrong_lang = 'it'
        self.request_data['language'] = wrong_lang
        expected_error_key = {'language'}

        response = self.client.patch(self.url, self.request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response.data.keys()), expected_error_key)
        self.assertEqual(
            response.data['language'],
            [ErrorDetail(string='Der Sprachenschlüssel ist nicht korrekt eingegeben', code='invalid')]
        )

    @override_settings(task_eager_propagates=True, task_always_eager=True, broker_url='memory://', backend='memory')
    def test_user_can_change_language_to_supported_language(self):
        self.client.force_authenticate(user=self.user)
        self.request_data['language'] = "en"
        expected_success_key = {'success'}
        expected_cookie_value = str({'language': 'en'})

        response = self.client.patch(self.url, self.request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.data.keys()), expected_success_key)
        self.assertEqual(response.data['success'], 'Your language has been successfully changed!')
        self.assertEqual(mail.outbox[0].subject, 'Language was changed!!!')
        self.assertEqual(mail.outbox[0].to, [self.user.email])
        self.assertEqual(response.cookies['django_language'].value, expected_cookie_value)
