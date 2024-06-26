from django.urls import path
from .views import (
    EventsView,
    EventView,
    AddEventView,
    UpdateEventView,
    DeleteEventView,
    AddRegistrationView,
    DeleteRegistrationView,
    event_calendar
)

urlpatterns = [
    path('', EventsView.as_view(), name='events'),
    path('<int:pk>', EventView.as_view(), name='event'),
    path('<int:event_id>/calendar/', event_calendar, name='event_calendar'),
    path('add/', AddEventView.as_view(), name='add_event'),
    path('<int:pk>/update/', UpdateEventView.as_view(), name='update_event'),
    path('<int:pk>/delete/', DeleteEventView.as_view(), name='delete_event'),
    path('<int:event_id>/add_registration/', AddRegistrationView.as_view(), name='add_registration'),
    path('<int:pk>/delete_registration/', DeleteRegistrationView.as_view(), name='delete_registration')
]
