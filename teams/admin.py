from django.contrib import admin
from .models import Team,TeamManager
# Register your models here.

admin.site.register(TeamManager)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    filter_horizontal = ('members',)