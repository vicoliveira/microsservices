from django.db import models
import uuid

from rest_framework.exceptions import ValidationError
from entrega.models import Entrega
from pedidos.utils import ufs
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone


class PedidoMannager(models.Manager):

    def create_pedido(self, **kwargs):
        try:

            kwargs["status"] = '1'
            entrega = Entrega.objects.get(uf=kwargs['uf'])

            pedido = self.create(
                **{
                    key: value for key, value in kwargs.items()
                    if key in [field.name for field in Pedido._meta.get_fields()]
                }
            )
            pedido.deliver_date = pedido.created_at + timedelta(days=entrega.sla)
            pedido.save()

        except Exception as e:
            raise ValidationError(e)

    def upgrade_when_sla_has_changed(self, **kwargs):
        try:
            pedidos = self.filter(~Q(status='3') & Q(uf=kwargs['uf']))
            for pedido in pedidos:
                pedido.deliver_date = pedido.created_at + timedelta(days=kwargs['sla'])

                pedido.save()

        except Exception as e:
            raise ValidationError(e)

    def confirm_delivery(self, pk, sts):
        try:
            pedido = self.get(pk=pk)
            if pedido.status == '3':
                return {'error': 'delivery status can not change'}

            if pedido.status == '2':
                pedido.deliver_date = timezone.now()

            pedido.status = sts
            pedido.save()
            return {"success": True}
        except Exception as e:
            raise ValidationError(e)


class Pedido(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    STATUS_CHOICES = (
        ('1', "Aguardando Pagamento"),
        ('2', "Em Rota"),
        ('3', "Entregue")
    )

    status = models.CharField("Status", choices=STATUS_CHOICES, default='1', max_length=1)
    created_at = models.DateTimeField(
        "Criado em",
        auto_now_add=True
    )
    deliver_date = models.DateTimeField('Data da entrega', blank=True, null=True)
    product = models.CharField("Nome do Produto", blank=True, null=True, max_length=100)
    address = models.CharField("Endereço", blank=True, null=True, max_length=100)
    uf = models.CharField("UFS", choices=ufs.STATE_CHOICES, blank=True, null=True, max_length=2)
    city = models.CharField("Cidade", blank=True, null=True, max_length=100)
    postal_code = models.CharField("CEP", blank=True, null=True, max_length=20)

    objects = PedidoMannager()
