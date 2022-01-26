from django.urls import path
from pcpanel.views import LoginView, BookingView, DeliveryView

urlpatterns = [
    path('', LoginView.as_view(), name='pclogin'),
    path('booking', BookingView.as_view(), name='pcbooking'),
    path('delivery', DeliveryView.as_view(), name='pcdelivery')
]