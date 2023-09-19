"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import (
    UserRegistrationView,
    UserProfileView,
    SendEmailConfirmationTokenAPIView,
    ConfirmEmailView,
    ChangePasswordView,
    ProfileUpdateView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    
    #authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('send-confirmation-email/', SendEmailConfirmationTokenAPIView.as_view(), name='send-confirmation-email'),
    path('confirm-email/', ConfirmEmailView.as_view(), name='confirm-email'),
    
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/',ChangePasswordView.as_view(),name='change-password'),
    path('profile-update/',ProfileUpdateView.as_view(),name='change-password'),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
