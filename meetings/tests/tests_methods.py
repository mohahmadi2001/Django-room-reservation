import unittest
from datetime import datetime,timedelta
from django.test import TestCase
from meetings.models import Room,RoomSlot
# Create your tests here.

class RoomSlotTestCase(TestCase):

    def setUp(self):
        self.room = Room.objects.create(name="Test Room", capacity=10)
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(hours=1)
        self.room_slot = RoomSlot.objects.create(room=self.room, start_time=self.start_time, end_time=self.end_time, is_empty=True)

    def test_get_room_status_in_time_range(self):
        result = RoomSlot.get_room_status_in_time_range(self.room, self.start_time, self.end_time)
        self.assertTrue(result) 
            
    def test_get_start_time(self):
        formatted_start_time = self.room_slot.get_start_time()
        expected_format = self.start_time.strftime('%Y-%m-%d %H:%M:%S')
        
        self.assertEqual(formatted_start_time, expected_format)

    def test_get_end_time(self):
        formatted_end_time = self.room_slot.get_end_time()
        expected_format = self.end_time.strftime('%Y-%m-%d %H:%M:%S')
        
        self.assertEqual(formatted_end_time, expected_format)

    
    def tearDown(self):
        self.room.delete()
        self.room_slot.delete()

if __name__ == '__main__':
    unittest.main()