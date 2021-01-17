from rest_framework import serializers

from core.models import Pet, Policy


class PetSerializer(serializers.ModelSerializer):
    """Serializer for a pet object"""

    class Meta:
        model = Pet
        fields = ('id', 'pet_name', 'pet_species', 'pet_breed', 'pet_age',)
        read_only_fields = ('id',)


class PolicySerializer(serializers.ModelSerializer):
    """Serializer for a policy object"""

    class Meta:
        model = Policy
        fields = (
            'policy_number', 'policy_premium',
        )
