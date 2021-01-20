from rest_framework import serializers


from core.models import Quate


class QuateSerializer(serializers.ModelSerializer):
    """Serialie a quate"""

    class Meta:
        model = Quate
        fields = (
            'quate_id',
        )
