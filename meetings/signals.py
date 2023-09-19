from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Room,RoomSlot

@receiver(pre_save, sender=Room)
def update_room_slot_status(sender, instance, **kwargs):
    """
    Signal handler to automatically update the RoomSlot status based on changes to the Room status.

    Args:
        sender (Room): The sender of the signal (Room model).
        instance (Room): The instance of the Room model being saved.
        **kwargs: Additional keyword arguments.

    Description:
        This signal handler is triggered before a Room instance is saved. It checks the status of the Room
        and updates the corresponding RoomSlots accordingly. If the Room status changes to "full," it updates
        the RoomSlot status to False (occupied). If the Room status changes to "empty," it updates the
        RoomSlot status to True (vacant).
    """
    if instance.status == 'full':
        RoomSlot.objects.filter(room=instance).update(is_empty=False)
    elif instance.status == 'empty':
        RoomSlot.objects.filter(room=instance).update(is_empty=True)
