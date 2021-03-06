from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

PAYLOAD = {
            'email': 'test@rainwalk.io',
            'password': 'testpass',
            'name': 'Name',
            'phone_number': '1234567899',
            'address_1': '123 Main st',
            'address_2': '#123',
            'city': 'Washington, D.C.',
            'zipcode': '12345',
            'state': 'DC',
}


def create_user(**params):
    """Helper function to create a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the useres API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with a vaild payload is successful"""
        payload = {
            'email': 'test@rainwalk.io',
            'password': 'testpass',
            'name': 'Name',
            'phone_number': '1234567899',
            'address_1': '123 Main st',
            'address_2': '#123',
            'city': 'Washington, D.C.',
            'zipcode': '12345',
            'state': 'DC',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {
            'email': 'test@rainwalk.io',
            'password': 'testpass',
            'name': 'Name',
            'phone_number': '1234567899',
            'address_1': '123 Main st',
            'address_2': '#123',
            'city': 'Washington, D.C.',
            'zipcode': '12345',
            'state': 'DC',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 5 characters"""
        payload = {
            'email': 'test@rainwalk.io',
            'password': 'pw',
            'name': 'Name',
            'phone_number': '1234567899',
            'address_1': '123 Main st',
            'address_2': '#123',
            'city': 'Washington, D.C.',
            'zipcode': '12345',
            'state': 'DC',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = PAYLOAD
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(
            email='test@rainwalk.io',
            password='wrong',
            name='Name',
            phone_number='1234567899',
            address_1='123 Main st',
            address_2='#123',
            city='Washington, D.C.',
            zipcode='12345',
            state='DC',
        )
        payload = PAYLOAD
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesnt exists"""
        payload = PAYLOAD
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='test@rainwalk.io',
            password='testpass',
            name='name',

        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieveing profile logged in users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'name': self.user.name,
            'phone_number': self.user.phone_number,
            'address_1': self.user.address_1,
            'address_2': self.user.address_2,
            'city': self.user.city,
            'zipcode': self.user.zipcode,
            'state': self.user.state,
        })

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me URL"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {
            'name': 'new name',
            'password': 'newpassword12345',
            'phone_number': '1111111111',
            'address_1': '123 Main st',
            'address_2': '#123',
            'city': 'Washington, D.C.',
            'zipcode': '12345',
            'state': 'DC',
        }
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(self.user.phone_number, payload['phone_number'])
        self.assertEqual(self.user.address_1, payload['address_1'])
        self.assertEqual(self.user.address_2, payload['address_2'])
        self.assertEqual(self.user.city, payload['city'])
        self.assertEqual(self.user.zipcode, payload['zipcode'])
        self.assertEqual(self.user.state, payload['state'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)
