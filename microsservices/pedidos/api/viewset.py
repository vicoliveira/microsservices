from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from ..models import Pedido
from utils.validator import ValidatorData
from django.shortcuts import get_object_or_404
from .serializer import PedidoSerializer


class PedidoView(ViewSet, ValidatorData):
    def __init__(self):
        self.pedido = Pedido
        self.status_accept = ('2', '3',)

    def create(self, request):
        required_fields = [
            "product",
            "address",
            "uf",
            "city",
            "postal_code"
        ]

        validator = self.validated_data(required_fields)

        if validator != 1:
            return validator

        self.pedido.objects.create_pedido(**request.data)

        return Response(
            {
                "success": True
            }, status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk=None):
        queryset = Pedido.objects.all()
        pedido = get_object_or_404(queryset, pk=pk)
        serializer = PedidoSerializer(pedido)
        return Response(serializer.data)

    def list(self, request, uf=None):
        try:
            queryset = Pedido.objects.filter(uf=uf)
            serializer = PedidoSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            ValidationError(e)

    def list_all(self, request):
        try:
            queryset = Pedido.objects.all()
            serializer = PedidoSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise ValidationError(e)

    def confirm_delivery_view(self, request, pk, sts):

        if sts not in self.status_accept:
            return Response(
                {
                    "error": f"Status code {sts} is not acceptable"
                }, status=status.HTTP_400_BAD_REQUEST
            )

        response = Pedido.objects.confirm_delivery(pk, sts)

        return Response(
            response,
            status.HTTP_200_OK if response.get("error", None) else status.HTTP_400_BAD_REQUEST
        )
