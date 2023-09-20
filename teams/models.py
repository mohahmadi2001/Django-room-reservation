from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Team(models.Model):
    name = models.CharField(_("name"), max_length=50)
    members = models.ManyToManyField(
        "users.CustomUser",
        verbose_name=_("members"),
        blank=True,
        related_name="team_members"
    )
    

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    def __str__(self):
        return self.name
    
    #create a new team
    @classmethod
    def create_team(cls, name, members=None):
        """
        Create a new team with the given name and members.

        Args:
            name (str): The name of the team.
            members (list of CustomUser, optional): List of team members (CustomUser objects).

        Returns:
            Team: The newly created Team object.
        """
        team = cls(name=name)
        team.save()
        if members:
            team.members.add(*members)
        return team

    #get all teams
    @classmethod
    def get_all_teams(cls):
        """
        Retrieve a list of all teams.

        Returns:
            QuerySet: A queryset containing all Team objects.
        """
        return cls.objects.all()
    
    #get all team members
    def get_team_members(self):
        """
        Retrieve a list of members for this team.

        Returns:
            QuerySet: A queryset containing CustomUser objects (members of the team).
        """
        return self.members.all()
    
    #update team members
    @classmethod
    def update_team(cls, team, name=None, members=None):
        """
        Update the attributes of a team.

        Args:
            team (Team): The team object to be updated.
            name (str, optional): The new name for the team.
            members (list of CustomUser, optional): List of team members (CustomUser objects).

        Returns:
            Team: The updated Team object.
        """
        if name:
            team.name = name
        if members is not None:
            team.members.clear()
            team.members.add(*members)
        team.save()
        return team


class TeamManager(models.Model):
    team = models.OneToOneField(
        Team,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='manager'
    )
    manager = models.ForeignKey(
        "users.CustomUser",
        verbose_name=_("manager"),
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.manager.username} Is Manager of {self.team.name} Team"
