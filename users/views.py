from rest_framework import status
from rest_framework.generics import CreateAPIView,UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
from .serializers import (
    UserRegistrationSerializer,
    UserInformationSerializer,
    ChangePasswordSerializer,
    UpdateProfileSerializer
)
from rest_framework.permissions import IsAuthenticated
from utils.confirmation_email_utils import send_confirmation_email
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationView(CreateAPIView):
    """
    User Registration View.

    This view allows users to register by providing their registration information. Upon successful registration, an email confirmation link is sent to the user's email address.

    - `POST`: Register a new user.

    Serializer:
    - `UserRegistrationSerializer`: Serializer for user registration data.

    Permissions:
    - None

    HTTP Status Codes:
    - 201 Created: Registration successful.
    - 400 Bad Request: Invalid data.

    """
    serializer_class = UserRegistrationSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"message": "Registration successful."}, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    User Profile View.

    This view allows authenticated users to retrieve their profile information.

    - `GET`: Retrieve the user's profile information.

    Permissions:
    - `IsAuthenticated`: Only authenticated users can access their profile.

    HTTP Status Codes:
    - 200 OK: Profile information retrieved successfully.

    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserInformationSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class SendEmailConfirmationTokenAPIView(APIView):
    """
    Send Email Confirmation Token View.

    This view allows users to request a new email confirmation token to be sent to their email address.

    - `POST`: Send a new email confirmation token.

    Permissions:
    - None

    HTTP Status Codes:
    - 200 OK: Email confirmation token sent successfully.

    """
    def post(self, request):
        user = request.user  
        send_confirmation_email(user)

        return Response({'message': 'An email confirmation link has been sent to your email address.'}, status=status.HTTP_200_OK)
    

class ConfirmEmailView(APIView):
    """
    Confirm Email View.

    This view allows users to confirm their email address using a confirmation token.

    - `GET`: Confirm the email address using a token.

    Permissions:
    - None

    HTTP Status Codes:
    - 200 OK: Email address successfully confirmed.
    - 400 Bad Request: Invalid confirmation token.

    """

    def get(self, request):
        token = request.GET.get('token', None)
        if token:
            try:
                access_token = AccessToken(token)
                user = User.objects.get(id=access_token['user_id'])
                user.is_email_confirmed = True
                user.save()
                return Response({'message': 'Email has been successfully confirmed.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': 'Invalid confirmation token.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Token is missing.'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """
    Change Password View.

    This view allows authenticated users to change their password.

    - `PUT`: Change the user's password.

    Permissions:
    - `IsAuthenticated`: Only authenticated users can change their password.

    HTTP Status Codes:
    - 200 OK: Password changed successfully.
    - 400 Bad Request: Invalid data or old password incorrect.

    """
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            confirm_new_password = serializer.validated_data['confirm_new_password']

            user = request.user

            if not user.check_password(old_password):
                return Response({'incorrect_password_error': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

            if new_password != confirm_new_password:
                return Response({'not_match_error': 'New passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ProfileUpdateView(UpdateAPIView):
    """
    Profile Update View.

    This view allows authenticated users to update their profile information.

    - `PUT`: Update the user's profile.

    Permissions:
    - `IsAuthenticated`: Only authenticated users can update their profile.

    HTTP Status Codes:
    - 200 OK: Profile updated successfully.

    """
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if 'email' in request.data and instance.email != request.data['email']:
            instance.is_email_confirmed = False
            return redirect('confirm-email') 
        return Response(serializer.data)