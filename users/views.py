from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer,UserInformationSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .utils import send_confirmation_email
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"message": "Registration successful."}, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserInformationSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class SendEmailConfirmationTokenAPIView(APIView):
    def post(self, request, format=None):
        user = request.user  
        send_confirmation_email(user)

        return Response({'message': 'An email confirmation link has been sent to your email address.'}, status=status.HTTP_200_OK)
    

class ConfirmEmailView(APIView):

    def get(self, request, format=None):
        token = request.GET.get('token', None)
        if token:
            try:
                access_token = AccessToken(token)
                user = get_user_model().objects.get(id=access_token['user_id'])
                user.is_email_confirmed = True
                user.save()
                return Response({'message': 'Email has been successfully confirmed.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': 'Invalid confirmation token.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Token is missing.'}, status=status.HTTP_400_BAD_REQUEST)
