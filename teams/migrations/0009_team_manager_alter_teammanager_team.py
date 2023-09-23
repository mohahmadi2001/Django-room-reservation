# Generated by Django 4.2.5 on 2023-09-23 08:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0008_alter_team_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_manager', to=settings.AUTH_USER_MODEL, verbose_name='manager'),
        ),
        migrations.AlterField(
            model_name='teammanager',
            name='team',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='team_manager', serialize=False, to='teams.team'),
        ),
    ]