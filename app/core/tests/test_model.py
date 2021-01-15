from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@rainwalk.io', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


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

    def test_pet_str(self):
        """Test the pet string representation"""
        pet = models.Pet.objects.create(
            user=sample_user(),
            pet_name='Test pet name',
            pet_species=1,
            pet_breed=2,
            pet_age=11
        )

        self.assertEqual(str(pet), pet.pet_name)
