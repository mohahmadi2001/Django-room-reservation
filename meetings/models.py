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
    

    class Meta:
        verbose_name = _("MeetingRoom")
        verbose_name_plural = _("MeetingRooms")

    def __str__(self):
        return self.name

