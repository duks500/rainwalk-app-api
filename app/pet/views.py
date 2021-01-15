from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Pet

from pet import serializers


class PetViewSet(viewsets.ModelViewSet):
    """Manage pets in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PetSerializer
    queryset = Pet.objects.all()

    def get_queryset(self):
        """Retrieve the pets for the authenticated user"""
        return self.queryset.filter(user=self.request.user)
