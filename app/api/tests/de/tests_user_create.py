from django.urls import reverse
from django.core import mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.test import APITestCase, override_settings
from app.models import User


class ProfileCreateTestCase(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('user_create')
        self.request_data = {
            'email': 'test2@test.com',
            'password': 'password',
            'language': 'de'
        }
        self.user = User.objects.create(email='test@test@com')

    @override_settings(task_eager_propagates=True, task_always_eager=True, broker_url='memory://', backend='memory')
    def test_user_with_german_language_created(self):
        response = self.client.post(self.url, self.request_data, format='json')
        expected_success_key = {'success'}

        user = get_object_or_404(User, email=self.request_data['email'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['success'], 'Sie haben erfolgreich ein Konto erstellt')
        self.assertEqual(set(response.data.keys()), set(expected_success_key))
        self.assertEqual(user.language, self.request_data['language'])
        self.assertEqual(mail.outbox[0].subject, 'Willkommen an Bord!!!')
        self.assertEqual(mail.outbox[0].to, [user.email])
