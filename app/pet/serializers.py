from rest_framework import serializers

from core.models import Policy


class PolicySerializer(serializers.ModelSerializer):
    """Serializer for a policy object"""

    class Meta:
        model = Policy
        fields = (
            'policy_number', 'policy_quate_number', 'policy_premium',
        )
