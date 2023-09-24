from django.urls import path
from .views import ReservationView,ReservationDeleteView

urlpatterns = [
    path('reserve/',ReservationView.as_view(),name="reservation-create"),
    path('<uuid:pk>/delete/', ReservationDeleteView.as_view(), name='reservation-delete'),
]
