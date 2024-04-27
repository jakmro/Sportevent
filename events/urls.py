from django.urls import path
from .views import (
    EventsView,
    EventView,
    AddEventView,
    UpdateEventView,
    DeleteEventView,
    EventRegistrationView
)

urlpatterns = [
    path('', EventsView.as_view(), name='events'),
    path('<int:pk>', EventView.as_view(), name='event'),
    path('add/', AddEventView.as_view(), name='add_event'),
    path('<int:pk>/update/', UpdateEventView.as_view(), name='update_event'),
    path('<int:pk>/delete/', DeleteEventView.as_view(), name='delete_event'),
    path('<int:pk>/register/', EventRegistrationView.as_view(), name='register_for_event')
]
