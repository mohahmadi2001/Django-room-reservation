from django.db import models
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Reservation(BaseModel):
    start_time = models.DateTimeField(_("start time"))
    end_time = models.DateTimeField(_("end time"))
    team = models.ForeignKey(
        "teams.Team",
        verbose_name=_("team"),
        on_delete=models.CASCADE,
        null=True,
        related_name="team_reservations"        
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
        return f"{self.team} Reserve for {self.room.name}"
    
    
    @classmethod
    def get_all_reservations(cls):
        """
        Retrieve a list of all reservations.

        Returns:
            QuerySet: A queryset containing all reservation objects.
        """
        return cls.objects.all()
    

    #get reservation for room
    @classmethod
    def get_room_reservations(cls, room):
        """
        Retrieve a list of reservations for a specific room.

        Args:
            room (Room): The room for which reservations are to be retrieved.

        Returns:
            QuerySet: A queryset containing reservation objects for the room.
        """
        return cls.objects.filter(room=room)
    


    def get_team_name(self):
        """
        Get the name of the team associated with this reservation.

        Returns:
            str or None: The name of the associated team or None if no team is associated.
        """
        return self.team.name if self.team else None

    def get_room_name(self):
        """
        Get the name of the room associated with this reservation.

        Returns:
            str or None: The name of the associated room or None if no room is associated.
        """
        return self.room.name if self.room else None