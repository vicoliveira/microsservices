from rest_framework import viewsets, status
from rest_framework.response import Response

from ..models import Entrega
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from utils.validator import ValidatorData
from django.shortcuts import get_object_or_404
from .serializer import EntregaSerializer


class EntregaView(ViewSet, ValidatorData):

    def create(self, request):
        required_fields = [
            'uf',
            'sla'
        ]

        validator = self.validated_data(required_fields)

        if validator != 1:
            return validator

        try:

            Entrega.objects.create(
                **{
                    key: value for key, value in request.data.items()
                    if key in [field.name for field in Entrega._meta.get_fields()]
                }
            )

            return Response({
                "success": True
            }, status=status.HTTP_200_OK
            )

        except Exception as e:
            raise ValidationError(e)

    def upgrade(self, request, uf=None, sla=None):
        try:
            queryset = Entrega.objects.all()
            entrega = get_object_or_404(queryset, uf=uf)
            entrega.sla = sla
            entrega.save()

            return Response({
                "success": True
            }, status=status.HTTP_200_OK
            )

        except Exception as e:
            raise ValidationError(e)

    def retrieve(self, request, uf=None):
        queryset = Entrega.objects.all()
        entrega = get_object_or_404(queryset, uf=uf)
        serializer = EntregaSerializer(entrega)
        return Response(serializer.data,  status=status.HTTP_200_OK)

    def list(self, request):
        try:
            queryset = Entrega.objects.all()
            serializer = EntregaSerializer(queryset, many=True)
            return Response(serializer.data,  status=status.HTTP_200_OK)
        except Exception as e:
            raise ValidationError(e)
