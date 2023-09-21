from rest_framework import permissions


class IsTeamManager(permissions.BasePermission):
    """
    Custom permission to only allow team managers to make reservations.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.team
            and request.user.team.is_manager(request.user)
        )
