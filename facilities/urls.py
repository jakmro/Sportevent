from django.urls import path
from .views import (
    FacilitiesView,
    FacilityView,
    AddFacilityView,
    AddRatingView,
    get_facilities_data,
    UpdateFacilityView,
    DeleteFacilityView,
    UpdateRatingView,
    DeleteRatingView,
    add_to_calendar
)

urlpatterns = [
    path('', FacilitiesView.as_view(), name='facilities'),
    path('<int:pk>', FacilityView.as_view(), name='facility'),
    path('<int:pk>/calendar/', add_to_calendar, name='add_to_calendar'),
    path('add/', AddFacilityView.as_view(), name='add_facility'),
    path('<int:facility_id>/add_rating/', AddRatingView.as_view(), name='add_rating'),
    path('<int:pk>/update_rating/', UpdateRatingView.as_view(), name='update_rating'),
    path('<int:pk>/delete_rating/', DeleteRatingView.as_view(), name='delete_rating'),
    path('<int:pk>/delete/', DeleteFacilityView.as_view(), name='delete_facility'),
    path('<int:pk>/update/', UpdateFacilityView.as_view(), name='update_facility'),
    path('data/', get_facilities_data, name='get_facilities_data')
]
