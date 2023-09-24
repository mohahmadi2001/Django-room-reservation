import unittest
from django.test import TestCase
from teams.models import Team, TeamManager
from users.models import CustomUser

class TeamModelTestCase(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create(username='user1')
        self.user2 = CustomUser.objects.create(username='user2')

        self.team = Team.objects.create(name='Test Team', manager=self.user1)
        self.team.members.add(self.user1, self.user2)

        self.team_manager = TeamManager.objects.create(team=self.team, manager=self.user1)

    def test_get_all_teams(self):
        teams = Team.get_all_teams()
        self.assertEqual(teams.count(), 1)
        self.assertEqual(teams[0], self.team)

    def test_get_team_members(self):
        members = self.team.get_team_members()
        self.assertEqual(members.count(), 2)
        self.assertIn(self.user1, members)
        self.assertIn(self.user2, members)


if __name__ == '__main__':
    unittest.main()