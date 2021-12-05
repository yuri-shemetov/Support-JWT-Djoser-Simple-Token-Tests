
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class TokenAuthUserProfileTestCase(APITestCase):
    main_url=reverse('main')
    def setUp(self):
        self.user=self.client.post('/auth/users/',data={'username':'dummy','password':'1234567!'})
        response=self.client.post('/auth/token/login/',data={'username':'dummy','password':'1234567!'})
        self.token=response.data['auth_token']
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token)

    # authentication is successful
    def test_userprofile_is_authenticated(self):
        response=self.client.get(self.main_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    # authentication isn't successful
    def test_userprofile_is_not_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response=self.client.get(self.main_url)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

class SimpleJwtUserProfileTestCase(APITestCase):
    main_url=reverse('main')
    def setUp(self):
        self.user=self.client.post('/auth/users/',data={'username':'dummy','password':'1234567!'})
        response=self.client.post('/auth/jwt/create/',data={'username':'dummy','password':'1234567!'})
        self.token=response.data['access']
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT '+self.token)

    # authentication is successful
    def test_userprofile_is_authenticated(self):
        response=self.client.get(self.main_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    # authentication isn't successful
    def test_userprofile_is_not_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response=self.client.get(self.main_url)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)