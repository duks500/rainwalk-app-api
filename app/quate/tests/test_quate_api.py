from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Quate

from quate.serializers import QuateSerializer


QUATE_URL = reverse('quate:quate-list')


def detail_url(quate_id):
    """Return quate detail URL"""
    return reverse('quate:quate-detail', args=[quate_id])


def sample_quate(quate_id):
    """Create a sample quate"""
    return Quate.objects.create(quate_id=quate_id)


class PublicQuateTests(TestCase):
    """Test unauthentivated quate API access"""

    def setUp(self):
        self.client = APIClient()

    def test_view_quate_detail(self):
        """Test viewing a quate detail"""
        quate = sample_quate('c83cbe43-5c30-4a5f-860b-5b8e9927ff8e')

        url = detail_url(quate.quate_id)
        res = self.client.get(url)

        serializer = QuateSerializer(quate)
        self.assertEqual(res.data, serializer.data)

    def test_create_quate_successful(self):
        """Test create a new quate"""
        payload = {
            'quate_id': 'c83cbe43-5c30-4a5f-860b-5b8e9927ff81',
        }
        self.client.post(QUATE_URL, payload)

        exists = Quate.objects.filter(
            quate_id=payload['quate_id']
        ).exists()

        self.assertTrue(exists)

    def test_create_quate_invalid(self):
        """Test creating invalid quate failed"""
        payload = {
            'quate_id': 'c83cbe43-5c30-4a5f-860b-5b8e9927ff81'
        }
        self.client.post(QUATE_URL, payload)
        res = self.client.post(QUATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
