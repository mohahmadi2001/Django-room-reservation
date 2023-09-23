from django.urls import path
from .views import TeamCreateView

urlpatterns = [
    path('create-team/', TeamCreateView.as_view({'get': 'list', 'post': 'create'}), name='create-team'),
]
