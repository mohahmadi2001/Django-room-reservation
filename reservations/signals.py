from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reservation
from meetings.models import RoomSlot

@receiver(post_save, sender=Reservation)
def create_room_slot(sender, instance, created, **kwargs):
    if created:
        RoomSlot.objects.create(
            room=instance.room,
            start_time=instance.start_time,
            end_time=instance.end_time,
            is_empty=False 
        )
