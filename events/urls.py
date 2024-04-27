from django.urls import path
from .views import (
    EventsView,
    EventView,
    AddEventView,
    UpdateEventView
)

urlpatterns = [
    path('', EventsView.as_view(), name='events'),
    path('<int:pk>', EventView.as_view(), name='event'),
    path('add/', AddEventView.as_view(), name='add_event'),
    path('<int:pk>/update/', UpdateEventView.as_view(), name='update_event'),
]
