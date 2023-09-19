from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class CustomUser(AbstractUser):
    class Meta:
        verbose_name = _("CustomUser")
        verbose_name_plural = _("CustomUsers")
        
    
