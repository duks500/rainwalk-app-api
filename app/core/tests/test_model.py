from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@rainwalk.io', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


def sample_quate(quate_id):
    """Create a sample quate"""
    return models.Quate.objects.create(quate_id=quate_id)


class ModelTest(TestCase):

    def test_create_user_with_email_successfult(self):
        """Test creating a new user with an email is successful"""
        email = 'test@rainwalk.io'
        password = 'Password12345'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@RAINWALK.io'
        user = get_user_model().objects.create_user(
            email=email,
            password='test123'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                None,
                'Test1234'
            )

    def test_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@rainwalk.io',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_policy_str(self):
        """Test the policy string representation"""
        quate = sample_quate('c83cbe43-5c30-4a5f-860b-5b8e9927ff8e')
        policy = models.Policy.objects.create(
            user=sample_user(),
            policy_number='PA-99999',
            policy_quate_number=quate
        )

        self.assertEqual(str(policy), policy.policy_number)

    def test_quate_str(self):
        """Test the quate string representation"""
        quate = models.Quate.objects.create(
            quate_id='8d60c12a-1ac5-4903-a1e3-0a3a4fc16989'
        )

        self.assertEqual(str(quate), quate.quate_id)
