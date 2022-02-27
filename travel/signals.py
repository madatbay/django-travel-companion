import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Budget, Trip

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Trip)
def create_budget(sender, instance, created, **kwargs):
    if created:
        instance = Budget.objects.create(trip=instance, name=f"{instance.name} Budget")
        if instance:
            logger.info(f"Bugdet instance <{instance.name}> created")
