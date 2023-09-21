from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import Team,TeamManager
from users.models import CustomUser

@receiver(m2m_changed, sender=Team.members.through)
def update_user_team(sender, instance, action, **kwargs):
    if action == 'post_add':
        for user in kwargs.get('pk_set', []):
            custom_user = CustomUser.objects.get(pk=user)
            custom_user.team = instance
            custom_user.save()