from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from .models import Reservation
from .serializers import ReservationSerializer,DeleteReservationSerializer
from .permissions import IsTeamManager
from rest_framework import generics, permissions
from utils.reminder_email_utils import send_reminder_email
from meetings.signals import delete_related_room_slots


class ReservationView(CreateAPIView):
    permission_classes = [IsTeamManager]
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            start_time = serializer.validated_data['start_time']
            end_time = serializer.validated_data['end_time']
            room = serializer.validated_data['room']
            team = serializer.validated_data['team']
            
            if Reservation.objects.filter(room=room, start_time__lte=end_time, end_time__gte=start_time).exists():
                return Response({'error': 'A reservation for this room in this time range already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            
            team_members = team.members.all()
            send_reminder_email(team_members, room, start_time, end_time)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReservationDeleteView(generics.DestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = DeleteReservationSerializer  
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        delete_related_room_slots(sender=Reservation, instance=instance)
        instance.delete()
        return Response({"message": "Reservation deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
