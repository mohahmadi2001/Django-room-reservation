from django.urls import path
from .views import (
    ActiveMeetingRoomsListView,
    RoomStatusView,
)

urlpatterns = [
     path('active-meeting-rooms/', ActiveMeetingRoomsListView.as_view(), name='active-meeting-rooms-list'),
     path('room-status/<uuid:room_id>/', RoomStatusView.as_view(), name='room-status-by-time'),
]
