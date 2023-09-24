from django.db.models.signals import post_save 
from django.dispatch import receiver
from .models import Team,TeamManager


@receiver(post_save, sender=Team)
def update_user_team_names(sender, instance, created, **kwargs):
    """
    A signal handler to update user team names when a team is created or updated.
    """
    if created:
        members = instance.members.all()
        for member in members:
            member.team = instance
            member.save()


@receiver(post_save, sender=TeamManager)
def set_user_as_team_manager(sender, instance, created, **kwargs):
    """
    A Signal handler to set a user as a team manager when a TeamManager instance is created.
    """
    if created:
        instance.manager.is_team_manager = True
        instance.manager.save()