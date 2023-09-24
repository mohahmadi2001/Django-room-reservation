from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import AbstractBaseModel

# Create your models here.

class Team(AbstractBaseModel):
    name = models.CharField(_("name"), max_length=50,unique=True)
    members = models.ManyToManyField(
        "users.CustomUser",
        verbose_name=_("members"),
        blank=True,
        related_name="team_members"
    )
    manager = models.ForeignKey(
        "users.CustomUser",
        verbose_name=_("manager"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="team_manager"
    )
    

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    def __str__(self):
        return self.name
    
    
    @classmethod
    def get_all_teams(cls):
        """
        Retrieve a list of all teams.

        Returns:
            QuerySet: A queryset containing all Team objects.
        """
        return cls.objects.all()
    
    def get_team_members(self):
        """
        Retrieve a list of members for this team.

        Returns:
            QuerySet: A queryset containing CustomUser objects (members of the team).
        """
        return self.members.all()
    


class TeamManager(models.Model):
    team = models.OneToOneField(
        Team,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='team_manager'
    )
    manager = models.ForeignKey(
        "users.CustomUser",
        verbose_name=_("manager"),
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.manager.username} Is Manager of {self.team.name} Team"
