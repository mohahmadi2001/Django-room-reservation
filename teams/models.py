from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Team(models.Model):
    name = models.CharField(_("name"), max_length=50)
    members = models.ManyToManyField(
        "users.CustomUser",
        verbose_name=_("member"),
        blank=True,
        related_name="team_members"
    )
    

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    def __str__(self):
        return self.name


