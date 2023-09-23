# Generated by Django 4.2.5 on 2023-09-23 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0010_alter_team_name'),
        ('users', '0009_alter_customuser_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='team',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='teams.team', verbose_name='team'),
        ),
    ]
