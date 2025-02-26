from django.test import TestCase
from rest_framework import response
from rest_framework.test import APIClient, APIRequestFactory


class TestUser(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.response = response
        self.signup_url = "/api/user/signup"

    def test_successful_user_signup(self):

        user = {
            "email":"coolemail@email.com",
            "username":"coolUser",
            "password":"Password123!",
            "password2":"Password123!"
        }

        self.response=self.client.post(self.signup_url, user, format='json')
        self.assertEqual(self.response.data['username'], 'coolUser')