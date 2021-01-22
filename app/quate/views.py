from rest_framework import viewsets

from core.models import Quate

from quate import serializers


class QuateViewSet(viewsets.ModelViewSet):
    """Manage quates in the database"""
    serializer_class = serializers.QuateSerializer
    queryset = Quate.objects.all()
