from .models import Team,TeamManager
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import TeamSerializer
from rest_framework import permissions
from users.models import CustomUser
from django.db import IntegrityError 


class TeamCreateView(viewsets.ModelViewSet):
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
            
            
            if team and manager:
                members = team.members.all()
                for member in members:
                    member.team = team
                    member.save()
            
            return Response(message, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
