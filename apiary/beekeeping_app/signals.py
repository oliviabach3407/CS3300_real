from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Hive, Calendar

#creates a calendar model ANYTIME a hive is created
@receiver(post_save, sender=Hive)
def create_calendar(sender, instance, created, **kwargs):
    if created:
        Calendar.objects.create(hive=instance)
