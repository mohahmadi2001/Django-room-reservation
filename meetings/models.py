from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Room(models.Model):
    STATUS_CHOICES = (
        ('empty', 'empty'),
        ('full', 'full'),
    )
    name = models.CharField(_("name"), max_length=50)
    status = models.CharField(_("status"), max_length=10,choices=STATUS_CHOICES,default="empty")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("MeetingRoom")
        verbose_name_plural = _("MeetingRooms")

    def __str__(self):
        return self.name

