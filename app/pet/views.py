from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Policy

from pet import serializers


class PolicyViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    """Manage polices in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Policy.objects.all()
    serializer_class = serializers.PolicySerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(
            user=self.request.user
        ).order_by('policy_number')

    def perform_create(self, serializer):
        """Create a new policy"""
        serializer.save(user=self.request.user)
