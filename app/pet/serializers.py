from rest_framework import serializers

from core.models import Pet, Policy


class PolicySerializer(serializers.ModelSerializer):
    """Serializer for a policy object"""

    class Meta:
        model = Policy
        fields = (
            'policy_number', 'policy_premium',
        )


class PetSerializer(serializers.ModelSerializer):
    """Serializer for a pet object"""

    pet_policy_premium = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Policy.objects.all()
    )

    class Meta:
        model = Pet
        fields = (
            'id',
            'pet_name',
            'pet_species',
            'pet_breed',
            'pet_age',
            'pet_policy_premium',
        )
        read_only_fields = ('id',)


class PetDetailSerializer(PetSerializer):
    """Serializer a pet detail"""
    pet_policy_premium = PolicySerializer(many=True, read_only=True)
