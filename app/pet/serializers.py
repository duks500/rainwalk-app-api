from rest_framework import serializers

from core.models import Pet, Policy


class PolicySerializer(serializers.ModelSerializer):
    """Serializer for a policy object"""

    class Meta:
        model = Policy
        fields = (
            'policy_number', 'policy_quate_number', 'policy_premium',
        )


class PetSerializer(serializers.ModelSerializer):
    """Serializer for a pet object"""

    # pet_policy_premium = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     queryset=Policy.objects.all()
    # )

    class Meta:
        model = Pet
        fields = (
            'pet_name',
            'pet_policy',
        )
        # read_only_fields = ('id',)


class PetDetailSerializer(PetSerializer):
    """Serializer a pet detail"""
    pet_policy = PolicySerializer(many=True, read_only=True)
