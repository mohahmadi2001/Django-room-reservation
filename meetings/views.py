from rest_framework.generics import ListAPIView
from .models import Room,RoomSlot
from .serializers import RoomSerializer,RoomSlotSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from rest_framework import status

class ActiveMeetingRoomsListView(ListAPIView):
    queryset = Room.objects.filter(is_active=True)  
    serializer_class = RoomSerializer


class RoomStatusView(APIView):
    def get(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
            room_slots = RoomSlot.objects.filter(room=room)
            serializer = RoomSlotSerializer(room_slots, many=True)
            
            serialized_data = serializer.data
            for slot_data in serialized_data:
                is_empty = RoomSlot.get_room_status_in_time_range(room, slot_data['start_time'], slot_data['end_time'])
                slot_data['status'] = "Empty" if is_empty else "Full"

            return Response(serialized_data, status=status.HTTP_200_OK)
        except Room.DoesNotExist:
            return Response({"error": "Room not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)