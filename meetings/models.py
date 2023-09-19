from django.db import models
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Room(BaseModel):
    STATUS_CHOICES = (
        ('empty', 'empty'),
        ('full', 'full'),
    )
    name = models.CharField(_("name"), max_length=50)
    status = models.CharField(_("status"), max_length=10,choices=STATUS_CHOICES,default="empty")
    capacity = models.PositiveIntegerField(_("capacity"))
    

    class Meta:
        verbose_name = _("MeetingRoom")
        verbose_name_plural = _("MeetingRooms")

    def __str__(self):
        return self.name
    
    #create Room
    @classmethod
    def create_room(cls, name, status="empty", capacity=0):
        """
        Create a new room with the given name, status, and capacity.

        Args:
            name (str): The name of the room.
            status (str, optional): The status of the room (default is "empty").
            capacity (int, optional): The capacity of the room (default is 0).

        Returns:
            Room: The newly created room object.
        """   
        room = cls(name=name, status=status, capacity=capacity)
        room.save()
        return room

    #get all room
    @classmethod
    def get_all_rooms(cls):
        """
        Retrieve a list of all available rooms.

        Returns:
            QuerySet: A queryset containing all room objects.
        """
        return cls.objects.all()
    
    #get empty room
    @classmethod
    def get_empty_rooms(cls):
        """
        Retrieve a list of all empty rooms.

        Returns:
            QuerySet: A queryset containing all empty room objects.
        """
        return cls.objects.filter(status="empty")
    
    #get full room
    @classmethod
    def get_full_rooms(cls):
        """
        Retrieve a list of all full rooms.

        Returns:
            QuerySet: A queryset containing all full room objects.
        """
        return cls.objects.filter(status="full")

    #get room by capacity
    @classmethod
    def get_rooms_by_capacity(cls, capacity):
        """
        Retrieve a list of rooms with a capacity greater than or equal to the specified value.

        Args:
            capacity (int): The minimum capacity of the rooms to retrieve.

        Returns:
            QuerySet: A queryset containing room objects that meet the capacity criteria.
        """   
        return cls.objects.filter(capacity__gte=capacity)

    #update room
    @classmethod
    def update_room(cls, room_id, name=None, status=None, capacity=None):
        """
        Update the attributes of a room.

        Args:
            room_id (uuid): The ID of the room to be updated.
            name (str, optional): The new name for the room.
            status (str, optional): The new status for the room.
            capacity (int, optional): The new capacity for the room.

        Returns:
            Room: The updated room object.
        """
        room = cls.objects.get(id=room_id)
        if name:
            room.name = name
        if status:
            room.status = status
        if capacity is not None:
            room.capacity = capacity
        room.save()
        return room
    
    
    
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

    #create room slot
    @classmethod
    def create_room_slot(cls, room, start_time, end_time, is_empty=True):
        """
        Create a new room slot with the given room, start time, end time, and empty status.

        Args:
            room (Room): The room for which the slot is being created.
            start_time (datetime): The start time of the slot.
            end_time (datetime): The end time of the slot.
            is_empty (bool, optional): The status of the slot (default is True).

        Returns:
            RoomSlot: The newly created room slot object.
        """
        room_slot = cls(room=room, start_time=start_time, end_time=end_time, is_empty=is_empty)
        room_slot.save()
        return room_slot
    
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
        

    
        