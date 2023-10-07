from rest_framework import status
from rest_framework.response import Response
from .models import Reservation
from .serializers import ReservationSerializer,DeleteReservationSerializer
from .permissions import IsTeamManager
from rest_framework import generics, permissions
from utils.reminder_email_utils import send_reminder_email
from meetings.signals import delete_related_room_slots


class ReservationView(generics.CreateAPIView):
    """
    A view for creating reservations.

    This view allows Team Managers to create reservations for meeting rooms. It checks if a reservation for the same room
    within the specified time range already exists and sends a reminder email to team members after a reservation is created.

    - `POST`: Create a new reservation.

    Permissions:
    - `IsTeamManager`: Only Team Managers can create reservations.

    Serializer:
    - `ReservationSerializer`: Serializer for reservation data.

    HTTP Status Codes:
    - 201 Created: Reservation created successfully.
    - 400 Bad Request: Invalid data or a conflicting reservation exists.

    """
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
    """
    A view for deleting reservations.

    This view allows administrators to delete reservations. Upon deletion, it also triggers the deletion of related room slots.

    - `DELETE`: Delete a reservation.

    Permissions:
    - `IsAdminUser`: Only administrators can delete reservations.

    Serializer:
    - `DeleteReservationSerializer`: Serializer for deletion requests.

    HTTP Status Codes:
    - 204 No Content: Reservation deleted successfully.
    - 404 Not Found: Reservation not found.

    """
    queryset = Reservation.objects.all()
    serializer_class = DeleteReservationSerializer  
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        delete_related_room_slots(sender=Reservation, instance=instance)
        instance.delete()
        return Response({"message": "Reservation deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
