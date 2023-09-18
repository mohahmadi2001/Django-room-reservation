from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.

class Reservation(models.Model):
    start_time = models.DateTimeField(_("start time"))
    end_time = models.DateTimeField(_("end time"))
    user = models.ForeignKey(
        User,
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
    