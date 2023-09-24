import unittest
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from teams.models import Team, TeamManager
from teams.views import TeamCreateView
from teams.serializers import TeamSerializer
from users.models import CustomUser

class TeamCreateViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin_user = CustomUser.objects.create(username='admin', is_staff=True)
        self.non_admin_user = CustomUser.objects.create(username='user')
        self.team_data = {
            'name': 'Test Team',
            'manager': self.admin_user.id,
            'members': [self.admin_user.id, self.non_admin_user.id]
        }
        self.serializer = TeamSerializer(data=self.team_data)
        self.serializer.is_valid()
        
    def test_create_team(self):
        request = self.factory.post('/teams/', self.team_data, format='json')
        request.user = self.admin_user
        view = TeamCreateView.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(Team.objects.count(), 0)
        self.assertEqual(TeamManager.objects.count(), 0)
        self.assertEqual(self.admin_user.team, Team.objects.first())
        self.assertEqual(self.non_admin_user.team, Team.objects.first())

    def test_create_team_with_existing_member(self):
        # تست برای ایجاد تیم با کاربری که عضو تیم دیگری است
        existing_team = Team.objects.create(name='Existing Team')
        self.non_admin_user.team = existing_team
        self.non_admin_user.save()

        request = self.factory.post('/teams/', self.team_data, format='json')
        request.user = self.admin_user
        view = TeamCreateView.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(Team.objects.count(), 1)
        self.assertEqual(TeamManager.objects.count(), 0)


if __name__ == '__main__':
    unittest.main()