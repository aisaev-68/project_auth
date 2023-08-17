from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from auth_app.models import UserProfile


class UserProfileAPITestCase(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(phone_number='1234567890')

    def test_get_user_profile(self):
        url = reverse('api_user_profile')  # Замените на имя URL вашей вьюшки
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['phone_number'], self.user.phone_number)

    def test_get_user_profile_not_found(self):
        url = reverse('api_user_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'User not found')


class ReferralListAPITestCase(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(phone_number='1234567890')
        self.referred_user = UserProfile.objects.create(phone_number='9876543210')
        self.user.referred_users.add(self.referred_user)

    def test_get_referred_users(self):
        url = reverse('api_referral_list')  # Замените на имя URL вашей вьюшки
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.referred_user.phone_number, response.data['referred_users'])

class AuthorizationPhoneViewTestCase(TestCase):
    def test_authorization_phone_view_post(self):
        client = Client()
        response = client.post(reverse('authorize_phone'), {'phone_number': '1234567890'})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Ожидаем редирект

class VerifyCodeViewTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(phone_number='1234567890', activation_code='1234')

    def test_verify_code_view_post_success(self):
        client = Client()
        response = client.post(reverse('verify_code'), {'activation_code': '1234'}, session={'phone_number': '1234567890', 'activation_code': '1234'})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Ожидаем редирект

    def test_verify_code_view_post_failure(self):
        client = Client()
        response = client.post(reverse('verify_code'), {'activation_code': '5678'}, session={'phone_number': '1234567890', 'activation_code': '1234'})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Ожидаем редирект

class InputInviteCodeViewTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(phone_number='1234567890', invite_code='ABCD')

    def test_input_invite_code_view_post_success(self):
        client = Client()
        response = client.post(reverse('input_invite_code'), {'invite_code': 'ABCD'}, session={'phone_number': '1234567890'})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Ожидаем редирект

    def test_input_invite_code_view_post_failure(self):
        client = Client()
        response = client.post(reverse('input_invite_code'), {'invite_code': 'EFGH'}, session={'phone_number': '1234567890'})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Ожидаем редирект

class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(phone_number='1234567890')

    def test_get_user_profile(self):
        client = Client()
        response = client.get(reverse('api_user_profile'), session={'phone_number': '1234567890'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['phone_number'], '1234567890')

    def test_get_user_profile_not_found(self):
        client = Client()
        response = client.get(reverse('api_user_profile'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'User not found')
