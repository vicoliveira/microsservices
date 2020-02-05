from rest_framework import serializers
from ..models import Pedido


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = [
            "id",
            "status",
            "created_at",
            "deliver_date",
            "product",
            "address",
            "uf",
            "city",
            "postal_code"
        ]

        read_only_fields = fields
