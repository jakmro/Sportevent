from django.urls import path

from .views import FacilitiesView, AddFacilityView, AddOpenHoursView, AddRatingView

urlpatterns = [
    path('', FacilitiesView.as_view(), name='facilities'),
    path('add/', AddFacilityView.as_view(), name='add_facility'),
    path('add_open_hours/', AddOpenHoursView.as_view(), name='add_open_hours'),
    path('add_rating/', AddRatingView.as_view(), name='add_rating'),
]
