import unittest
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from meetings.models import Room,RoomSlot
from datetime import datetime, timedelta

class ActiveMeetingRoomsListViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('active-meeting-rooms-list') 

    def test_active_meeting_rooms_list(self):
        Room.objects.create(name="Active Room", is_active=True, capacity=10)
        Room.objects.create(name="Inactive Room", is_active=False, capacity=5)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    
    def tearDown(self):
        Room.objects.filter(name="Active Room").delete()
        Room.objects.filter(name="Inactive Room").delete()
        
        
if __name__ == '__main__':
    unittest.main()