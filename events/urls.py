from django.urls import path
from .views import (
    EventsView,
    AddEventView,
    UpdateEventView
)

urlpatterns = [
    path('', EventsView.as_view(), name='events'),
    path('add/', AddEventView.as_view(), name='add_event'),
    path('<int:pk>/update/', UpdateEventView.as_view(), name='update_event'),
]
