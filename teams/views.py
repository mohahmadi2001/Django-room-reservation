from .models import Team,TeamManager
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import TeamSerializer
from rest_framework import permissions
from django.db import IntegrityError 


class TeamCreateView(viewsets.ModelViewSet):
    """
    A view for creating teams.

    This view allows administrators to create teams. When a team is created, it also assigns a manager to the team and adds team members. It ensures that a user cannot be a member of more than one team.

    - `POST`: Create a new team.

    Permissions:
    - `IsAdminUser`: Only administrators can create teams.

    Serializer:
    - `TeamSerializer`: Serializer for team data.

    HTTP Status Codes:
    - 201 Created: Team created successfully.
    - 400 Bad Request: Invalid data or user already a member of another team.

    """
    permission_classes = [permissions.IsAdminUser]
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                self.perform_create(serializer)
            except IntegrityError:
               
                return Response(
                    {"message": "User is already a member of another team."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            message = {"message": "Team created successfully."}
            team = serializer.instance
            manager = serializer.validated_data.get('manager')
            TeamManager.objects.create(team=team, manager=manager)
            
            
            if team:
                members = team.members.all()
                for member in members:
                    member.team = team
                    member.save()
            
            return Response(message, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
