from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _

# Create your models here.

class CustomUser(AbstractUser):
    is_email_confirmed = models.BooleanField(_("email confirmed"),default=False)
    team = models.ForeignKey(
        "teams.Team",  
        verbose_name=_("team"),
        null=True,  
        blank=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = _("CustomUser")
        verbose_name_plural = _("CustomUsers")
        
    
