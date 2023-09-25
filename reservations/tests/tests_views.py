import unittest
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from reservations.models import Reservation
from teams.models import Team
from meetings.models import Room
from django.utils import timezone
from users.models import CustomUser  
from rest_framework_simplejwt.tokens import RefreshToken

class ReservationViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.team = Team.objects.create(name="Test Team")
        self.room = Room.objects.create(name="Test Room", capacity=10)
        self.reservation_data = {
            'start_time': timezone.now(),
            'end_time': timezone.now() + timezone.timedelta(hours=2),
            'team': self.team.id,
            'room': self.room.id,
        }

    def test_create_reservation(self):
        url = reverse('reservation-create')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(url, self.reservation_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
class ReservationDeleteViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.team = Team.objects.create(name="Test Team")
        self.room = Room.objects.create(name="Test Room", capacity=10)
        self.reservation = Reservation.objects.create(
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=2),
            team=self.team,
            room=self.room,
        )

    def test_delete_reservation(self):
        url = reverse('reservation-delete', args=[self.reservation.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Reservation.objects.filter(id=self.reservation.id).exists())

if __name__ == '__main__':
    unittest.main()