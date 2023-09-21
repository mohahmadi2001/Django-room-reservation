from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    team_name = serializers.ReadOnlyField(source='get_team_name')
    room_name = serializers.ReadOnlyField(source='get_room_name')

    class Meta:
        model = Reservation
        exclude = ("is_deleted","created_at","updated_at")
        
