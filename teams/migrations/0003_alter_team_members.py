# Generated by Django 4.2.5 on 2023-09-20 07:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0002_teammanager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='team_members', to=settings.AUTH_USER_MODEL, verbose_name='members'),
        ),
    ]
