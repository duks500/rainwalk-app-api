from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Pet

from pet.serializers import PetSerializer


PET_URL = reverse('pet:pet-list')


def detail_url(pet_id):
    """Return pet detail URL"""
    return reverse('pet:pet-detail', args=[pet_id])


def sample_pet(user, **params):
    """Create and return a sample pet"""
    defaults = {
        'pet_name': 'Pet name2',
        'pet_species': 1,
        'pet_breed': 1,
        'pet_age': '9'
    }
    defaults.update(params)

    return Pet.objects.create(user=user, **defaults)


class PublicPetpeApiTests(TestCase):
    """Test unauthenticated pet API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(PET_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRPeteApiTests(TestCase):
    """Test authenticated pet API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test2@rainwalk.io',
            password='test12345',
            name='Name',
            phone_number='1234567899',
            zipcode='12345'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_pets(self):
        """Test retrieving a list of pets"""
        sample_pet(user=self.user)
        sample_pet(user=self.user)

        res = self.client.get(PET_URL)

        # .order_by('-id')
        pets = Pet.objects.all()
        serializer = PetSerializer(pets, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_pets_limited_user(self):
        """Test retrieving pet for user"""
        user2 = get_user_model().objects.create_user(
            email='test1@rainwalk.io',
            password='test12345',
            name='Name',
            phone_number='1234567899',
            zipcode='12345'
        )
        sample_pet(user=user2)
        sample_pet(user=self.user)

        res = self.client.get(PET_URL)

        pets = Pet.objects.filter(user=self.user)
        serializer = PetSerializer(pets, many=True)

        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
