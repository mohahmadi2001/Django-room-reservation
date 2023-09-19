from django.db import models
from core.models import AbstractBaseModel
from django.utils.translation import gettext_lazy as _

# Create your models here.

class CustomUser(AbstractBaseModel):
    class Meta:
        verbose_name = _("CustomUser")
        verbose_name_plural = _("CustomUsers")
        
    
