from django.urls import path
from .views import (
    FacilitiesView,
    FacilityView,
    AddFacilityView,
    AddRatingView,
    UpdateFacilityView,
    DeleteFacilityView,
    UpdateRatingView,
    DeleteRatingView,
    facility_calendar
)

urlpatterns = [
    path('', FacilitiesView.as_view(), name='facilities'),
    path('<int:pk>', FacilityView.as_view(), name='facility'),
    path('<int:pk>/calendar/', facility_calendar, name='facility_calendar'),
    path('add/', AddFacilityView.as_view(), name='add_facility'),
    path('<int:facility_id>/add_rating/', AddRatingView.as_view(), name='add_rating'),
    path('<int:pk>/update_rating/', UpdateRatingView.as_view(), name='update_rating'),
    path('<int:pk>/delete_rating/', DeleteRatingView.as_view(), name='delete_rating'),
    path('<int:pk>/delete/', DeleteFacilityView.as_view(), name='delete_facility'),
    path('<int:pk>/update/', UpdateFacilityView.as_view(), name='update_facility')
]
