from django.urls import path
from .views import room

urlpatterns = [
    path('<uidb64>/', room, name='room'),
]
