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
    serializer_class = UserRegistrationSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"message": "Registration successful."}, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserInformationSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class SendEmailConfirmationTokenAPIView(APIView):
    def post(self, request):
        user = request.user  
        send_confirmation_email(user)

        return Response({'message': 'An email confirmation link has been sent to your email address.'}, status=status.HTTP_200_OK)
    

class ConfirmEmailView(APIView):

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