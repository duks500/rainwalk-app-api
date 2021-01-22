from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Policy, Quate

from pet.serializers import PolicySerializer


POLICY_URL = reverse('pet:policy-list')


def detail_url(policy_id):
    """Return policy deatil URL"""
    return reverse('pet:policy-detail', args=[policy_id])


def sample_quate(quate_id):
    """Create a sample quate"""
    return Quate.objects.create(quate_id=quate_id)


def sample_policy(user, **params):
    """Create and return a sample polciy"""
    quate1 = sample_quate('be1795f2-2921-47bc-af26-e9bbcdd12fc0')
    defaults = {
        'policy_premium': 1,
        'policy_quate_number': quate1,
    }
    defaults.update(params)

    return Policy.objects.create(user=user, **defaults)


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
        quate1 = sample_quate('be1795f2-2921-47bc-af26-e9bbcdd12fc8')
        quate2 = sample_quate('697fa3a0-23b1-4e41-9af2-70980a719cf3')
        Policy.objects.create(
            user=self.user,
            policy_number='PA-12345',
            policy_quate_number=quate1
        )
        Policy.objects.create(
            user=self.user,
            policy_number='PA-54321',
            policy_quate_number=quate2
        )

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
        quate1 = sample_quate('be1795f2-2921-47bc-af26-e9bbcdd12fc8')
        Policy.objects.create(
            user=user2,
            policy_number='PA-99999',
            policy_quate_number=quate1,
        )
        quate2 = sample_quate('697fa3a0-23b1-4e41-9af2-70980a719cf3')
        policy = Policy.objects.create(
            user=self.user,
            policy_number='PA-12345',
            policy_quate_number=quate2,
        )

        res = self.client.get(POLICY_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['policy_number'], policy.policy_number)

    # def test_view_policy_detail(self):
    #     """Test viewing a policy detail"""
    #     quate1 = sample_quate('be1795f2-2921-47bc-af26-e9bbcdd12f11')
    #     policy = Policy.objects.create(
    #         user=self.user,
    #         policy_number='PA-ZZZZZ',
    #         policy_quate_number=quate1,
    #     )
    #     url = detail_url(policy)
    #     serializer = PolicySerializer(policy.policy_number)
    #
    #     self.assertEqual(res.data, serializer.data)

    def test_create_policy_successful(self):
        """Test creating a new policy"""
        quate1 = sample_quate('be1795f2-2921-47bc-af26-e9bbcdd12fc8')
        payload = {
            'policy_premium': 1,
            'policy_quate_number': quate1,
        }
        self.client.post(POLICY_URL, payload)

        exists = Policy.objects.filter(
            user=self.user,
            policy_premium=payload['policy_premium']
        ).exists()

        self.assertTrue(exists)

    def test_create_policy_invalid(self):
        """Test creating an invalid policy fails"""
        quate1 = sample_quate('be1795f2-2921-47bc-af26-e9bbcdd12fc8')
        payload = {
            'policy_premium': 3,
            'policy_quate_number': quate1,
        }

        res = self.client.post(POLICY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_policies_by_quates(self):
        """Test returing policy with specific quate number"""
        policy1 = sample_policy(user=self.user, policy_premium=1)
        quate1 = sample_quate('be1795f2-2921-47bc-af26-e9bbcdd12fc8')
        # policy1.policy_quate_number_set.create()

        res = self.client.get(
            POLICY_URL,
            {'policy_quate_number': f'{quate1}'}
        )

        serializer1 = PolicySerializer(policy1)

        self.assertIn(serializer1.data, res.data)
