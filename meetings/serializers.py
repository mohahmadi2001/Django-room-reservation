from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Room,RoomSlot

User = get_user_model()


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name', 'capacity','is_active')



class RoomSlotSerializer(serializers.ModelSerializer):
    room_name = serializers.CharField(source='room.name', read_only=True)
    class Meta:
        model = RoomSlot
        exclude = ('room','is_empty',)
        
        