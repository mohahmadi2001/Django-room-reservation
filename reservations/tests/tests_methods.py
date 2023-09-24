import unittest
from django.test import TestCase
from teams.models import Team
from meetings.models import Room
from reservations.models import Reservation
from django.utils import timezone

class ReservationModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="Test Team")

        self.room = Room.objects.create(name="Test Room", capacity=10)

        self.reservation = Reservation.objects.create(
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=2),
            team=self.team,
            room=self.room,
        )

    def test_get_all_reservations(self):
        total_reservations = Reservation.objects.count()

        reservations = Reservation.get_all_reservations()
        self.assertEqual(reservations.count(), total_reservations)

    def test_get_room_reservations(self):
        room_reservations = Reservation.get_room_reservations(self.room)
        self.assertEqual(room_reservations.count(), 1)

    def test_get_team_name(self):
        team_name = self.reservation.get_team_name()
        self.assertEqual(team_name, "Test Team")

    def test_get_room_name(self):
        room_name = self.reservation.get_room_name()
        self.assertEqual(room_name, "Test Room")

if __name__ == '__main__':
    unittest.main()