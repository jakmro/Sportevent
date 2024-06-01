from django.urls import path
from .views import (
    MapFacilitiesView,
    MapEventsView,
    get_facilities_data,
    get_meetings_data
)

urlpatterns = [
    path('facilities/', MapFacilitiesView.as_view(), name='maps_facilities'),
    path('events/', MapEventsView.as_view(), name='maps_events'),
    path('facilities_data/', get_facilities_data, name='get_facilities_data'),
    path('meetings_data/', get_meetings_data, name='get_meetings_data')
]
