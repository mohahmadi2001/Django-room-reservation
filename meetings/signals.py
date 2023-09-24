from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import RoomSlot
from reservations.models import Reservation


@receiver(post_delete, sender=Reservation)
def delete_related_room_slots(sender, instance, **kwargs):
    """
    A Signal handler to delete related room slots when a reservation is deleted.
    """
    RoomSlot.objects.filter(room=instance.room, start_time=instance.start_time, end_time=instance.end_time).delete()