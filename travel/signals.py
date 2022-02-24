from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Budget, Trip


@receiver(post_save, sender=Trip)
def create_budget(sender, instance, created, **kwargs):
    if created:
        Budget.objects.create(trip=instance, name=f"{instance.name} Budget")
