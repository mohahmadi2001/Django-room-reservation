from django.db import models
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Room(BaseModel):
    name = models.CharField(_("name"), max_length=50)
    is_active = models.BooleanField(_("is_active"), default="True")
    capacity = models.PositiveIntegerField(_("capacity"))
    

    class Meta:
        verbose_name = _("MeetingRoom")
        verbose_name_plural = _("MeetingRooms")

    def __str__(self):
        return self.name
    
       
class RoomSlot(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name=_("room"))
    start_time = models.DateTimeField(_("start time"))
    end_time = models.DateTimeField(_("end time"))
    is_empty = models.BooleanField(_("is empty"), default=True)

    class Meta:
        verbose_name = _("Room Slot")
        verbose_name_plural = _("Room Slots")

    def __str__(self):
        return f"{self.room.name} - {self.start_time} to {self.end_time}"

    
    #get room status in time range
    @classmethod
    def get_room_status_in_time_range(cls, room, start_time, end_time):
        """
        Retrieve the status of a room within a specified time range.

        Args:
            room (Room): The room for which the status is requested.
            start_time (datetime): The start time of the time range.
            end_time (datetime): The end time of the time range.

        Returns:
            bool: True if the room is empty within the specified time range, False otherwise.
        """
        room_slot = cls.objects.get(room=room, start_time=start_time, end_time=end_time)
        return room_slot.is_empty
    
    
    def update_room_status_in_time_range(cls, room, start_time, end_time):
        """
        Update the status of the room for a specified time range.

        Args:
            room (Room): The room for which the status is updated.
            start_time (datetime): The start time of the time range.
            end_time (datetime): The end time of the time range.

        Returns:
            bool: True if the room status was updated successfully, False otherwise.
        """
        try:
            room_slot = cls.objects.get(room=room, start_time=start_time, end_time=end_time)
            room_slot.is_empty = False  
            room_slot.save()
            return True
        except cls.DoesNotExist:
            return False
  
    def get_start_time(self):
        """
        Return the start time in a formatted string.
        """
        return self.start_time.strftime('%Y-%m-%d %H:%M:%S')

    def get_end_time(self):
        """
        Return the end time in a formatted string.
        """
        return self.end_time.strftime('%Y-%m-%d %H:%M:%S')      

    
        