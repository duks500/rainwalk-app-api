from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Policy

from pet.serializers import PolicySerializer


POLICY_URL = reverse('pet:policy-list')


class PublicPoliciesApiTests(TestCase):
    """Test the publically availpable policies API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access this endpoint"""
        res = self.client.get(POLICY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePoliciesAPITests(TestCase):
    """Test policies can be retrieved by authrotized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@rainwalk.io',
            'password12345'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_policy_list(self):
        """Test retrieving a list of policies"""
        Policy.objects.create(user=self.user, policy_number='PA-12345')
        Policy.objects.create(user=self.user, policy_number='PA-54321')

        res = self.client.get(POLICY_URL)

        policies = Policy.objects.all()
        serializer = PolicySerializer(policies, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_policies_limited_to_user(self):
        """Test that only policies for authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            'other@rainwalk.io',
            'testpass12345',
        )

        Policy.objects.create(user=user2, policy_number='PA-99999')
        policy = Policy.objects.create(
            user=self.user,
            policy_number='PA-12345'
        )

        res = self.client.get(POLICY_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['policy_number'], policy.policy_number)

    def test_create_policy_successful(self):
        """Test creating a new policy"""
        payload = {
            'policy_premium': 1,
        }
        self.client.post(POLICY_URL, payload)

        exists = Policy.objects.filter(
            user=self.user,
            policy_premium=payload['policy_premium']
        ).exists()

        self.assertTrue(exists)

    def test_create_policy_invalid(self):
        """Test creating an invalid policy fails"""
        payload = {
            'policy_premium': 3,
        }

        res = self.client.post(POLICY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
