from rest_framework import serializers
from .models import Team
from users.models import CustomUser

class TeamSerializer(serializers.ModelSerializer):
    manager = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)

    class Meta:
        model = Team
        fields = '__all__'
