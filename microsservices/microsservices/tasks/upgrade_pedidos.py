from celery.task import task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@task(name='upgrade_deliver_when_sla_has_changed_task', autoretry_for=(Exception,), retry_backoff=True)
def upgrade_deliver_when_sla_has_changed_task(**kwargs):
    from pedidos.models import Pedido
    logger.info('Upgrade deliver when sla has changed_task')
    Pedido.objects.upgrade_when_sla_has_changed(**kwargs)
