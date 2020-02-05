import uuid

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from pedidos.utils import ufs
from celery import chain
from microsservices.tasks.upgrade_pedidos import upgrade_deliver_when_sla_has_changed_task
from model_utils import FieldTracker


class Entrega(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    uf = models.CharField("UFS", choices=ufs.STATE_CHOICES, blank=True, null=True, max_length=2, unique=True)
    sla = models.IntegerField("SLA", default=0)
    tracker = FieldTracker()

    def __str__(self):
        return f'{self.uf} --- {self.sla}'


@receiver(post_save, sender=Entrega, dispatch_uid="create_update_iugu")
def upgrade_pedidos(sender, **kwargs):
    if not kwargs['created']:
        entrega = kwargs['instance']

        if entrega.tracker.changed().get('sla', None):
            action = chain(
                upgrade_deliver_when_sla_has_changed_task.si(**{
                    'uf': entrega.uf,
                    'sla': entrega.sla
                }),
            )

            action.delay()
