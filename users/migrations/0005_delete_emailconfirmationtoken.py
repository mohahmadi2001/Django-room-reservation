# Generated by Django 4.2.5 on 2023-09-19 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_is_email_confirmed'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EmailConfirmationToken',
        ),
    ]
