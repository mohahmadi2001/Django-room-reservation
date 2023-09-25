from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import AbstractBaseModel
from django.utils.translation import gettext_lazy as _

# Create your models here.

class CustomUser(AbstractUser,AbstractBaseModel):
    is_email_confirmed = models.BooleanField(_("email confirmed"),default=False)
    is_team_manager = models.BooleanField(_("team manager"),default=False)
    team = models.ForeignKey(
        "teams.Team",  
        verbose_name=_("team"),
        null=True,  
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = _("CustomUser")
        verbose_name_plural = _("CustomUsers")
        
    
