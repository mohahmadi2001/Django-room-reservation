from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .serializers import CustomRegistrationSerializer

class UserRegistrationView(CreateAPIView):
    serializer_class = CustomRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"message": "Registration successful."}, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
