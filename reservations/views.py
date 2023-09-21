from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from meetings.models import  RoomSlot, Room
from teams.models import Team
from .models import Reservation
from .serializers import ReservationSerializer

class ReservationView(CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            start_time = serializer.validated_data['start_time']
            end_time = serializer.validated_data['end_time']
            room = serializer.validated_data['room']
            
            if Reservation.objects.filter(room=room, start_time__lte=end_time, end_time__gte=start_time).exists():
                return Response({'error': 'A reservation for this room in this time range already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
