from django.urls import path
from .views import ReservationView

urlpatterns = [
    path('reserve/',ReservationView.as_view(),name="reservation")
]
