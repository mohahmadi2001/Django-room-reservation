from django.db import models
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Reservation(BaseModel):
    start_time = models.DateTimeField(_("start time"))
    end_time = models.DateTimeField(_("end time"))
    user = models.ForeignKey(
        "users.CustomUser",
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="user_reservations"        
    )
    room = models.ForeignKey(
        "meetings.Room",
        verbose_name=_("room"),
        on_delete=models.CASCADE,
        related_name="room_reservations"
    )
    

    class Meta:
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")

    def __str__(self):
        return f"{self.user.username} Reserve for {self.room.name}"
    
    #create a reservation
    def create_reservation(start_time, end_time, user, room):
        """
        Create a new reservation for a specified time range, user, and room.

        Args:
            start_time (datetime): The start time of the reservation.
            end_time (datetime): The end time of the reservation.
            user (CustomUser): The user making the reservation.
            room (Room): The room being reserved.

        Returns:
            Reservation: The newly created reservation object.
        """
        reservation = Reservation(start_time=start_time, end_time=end_time, user=user, room=room)
        reservation.save()
        return reservation
    
    #get all reservation
    def get_all_reservations():
        """
        Retrieve a list of all reservations.

        Returns:
            QuerySet: A queryset containing all reservation objects.
        """
        return Reservation.objects.all()
    
    #get reservation for user
    def get_user_reservations(user):
        """
        Retrieve a list of reservations made by a specific user.

        Args:
            user (CustomUser): The user whose reservations are to be retrieved.

        Returns:
            QuerySet: A queryset containing reservation objects made by the user.
        """
        return Reservation.objects.filter(user=user)

    #get reservation for room
    def get_room_reservations(room):
        """
        Retrieve a list of reservations for a specific room.

        Args:
            room (Room): The room for which reservations are to be retrieved.

        Returns:
            QuerySet: A queryset containing reservation objects for the room.
        """
        return Reservation.objects.filter(room=room)

    #update reservation
    def update_reservation(reservation, start_time=None, end_time=None, user=None, room=None):
        """
        Update the attributes of a reservation.

        Args:
            reservation (Reservation): The reservation object to be updated.
            start_time (datetime, optional): The new start time for the reservation.
            end_time (datetime, optional): The new end time for the reservation.
            user (CustomUser, optional): The new user for the reservation.
            room (Room, optional): The new room for the reservation.

        Returns:
            Reservation: The updated reservation object.
        """
        if start_time:
            reservation.start_time = start_time
        if end_time:
            reservation.end_time = end_time
        if user:
            reservation.user = user
        if room:
            reservation.room = room
        reservation.save()
        return reservation
