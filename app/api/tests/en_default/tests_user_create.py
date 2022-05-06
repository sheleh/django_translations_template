from django.urls import reverse
from django.core import mail
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase, override_settings
from app.models import User


class ProfileCreateTestCase(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('user_create')
        self.request_data = {
            'email': 'test2@test.com',
            'password': 'password',
        }
        self.user = User.objects.create(email='test@test.com')

    def test_all_fields_are_blank(self):
        self.request_data['email'] = ''
        self.request_data['password'] = ''
        expected_error_keys = {'email', 'password'}

        response = self.client.post(self.url, self.request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response.data.keys()), set(expected_error_keys))
        self.assertEqual(response.data['email'],
                         [ErrorDetail(string='This field may not be blank.', code='blank')])
        self.assertEqual(response.data['password'],
                         [ErrorDetail(string='This field may not be blank.', code='blank')])

    def test_email_field_are_incorrectly_filled(self):
        self.request_data['email'] = 'this is my email'
        expected_error_key = {'email'}

        response = self.client.post(self.url, self.request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response.data.keys()), set(expected_error_key))
        self.assertEqual(response.data['email'],
                         [ErrorDetail(string='Enter a valid email address.', code='invalid')]
                         )

    def test_required_fields_are_not_sent(self):
        request_data = {}
        expected_error_keys = {'email', 'password'}

        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'],
                         [ErrorDetail(string='This field is required.', code='required')])
        self.assertEqual(response.data['password'],
                         [ErrorDetail(string='This field is required.', code='required')])
        self.assertEqual(set(response.data.keys()), set(expected_error_keys))

    def test_user_with_wrong_language_not_created(self):
        wrong_language_code = 'xx'
        self.request_data['language'] = wrong_language_code
        response = self.client.post(self.url, self.request_data, format='json')
        expected_success_key = {'language'}

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['language'],
            [ErrorDetail(string=f'"{wrong_language_code}" is not a valid choice.', code='invalid_choice')]
        )
        self.assertEqual(set(response.data.keys()), set(expected_success_key))

    @override_settings(task_eager_propagates=True, task_always_eager=True, broker_url='memory://', backend='memory')
    def test_user_with_default_language_created(self):
        response = self.client.post(self.url, self.request_data, format='json')
        expected_success_key = {'success'}

        user = get_object_or_404(User, email=self.request_data['email'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['success'], 'You have successfully created account !')
        self.assertEqual(set(response.data.keys()), set(expected_success_key))
        self.assertEqual(user.language, settings.LANGUAGE_CODE[:2])
        self.assertEqual(mail.outbox[0].subject, 'Welcome on board!!!')
        self.assertEqual(mail.outbox[0].to, [user.email])
