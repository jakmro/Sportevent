from django.urls import path
from .views import (
    EventsView,
    AddEventView
)

urlpatterns = [
    path('', EventsView.as_view(), name='events'),
    path('add/', AddEventView.as_view(), name='add_event'),
]
