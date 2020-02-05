from rest_framework import serializers
from ..models import Entrega


class EntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrega
        fields = [
            "id",
            "uf",
            "sla"
        ]

        read_only_fields = fields
