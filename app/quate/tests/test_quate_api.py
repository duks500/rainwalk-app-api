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


def sample_quate(**params):
    """Create and return a sample pet"""
    defaults = {
        'quate_id': 'c83cbe43-5c30-4a5f-860b-5b8e9927ff8e',
    }
    defaults.update(params)

    return Quate.objects.create(**defaults)


class PublicQuateTests(TestCase):
    """Test unauthentivated quate API access"""

    def setUp(self):
        self.client = APIClient()

    def test_view_quate_detail(self):
        """Test viewing a quate detail"""
        quate = sample_quate()

        url = detail_url(quate.quate_id)
        res = self.client.get(url)

        serializer = QuateSerializer(quate)
        self.assertEqual(res.data, serializer.data)
