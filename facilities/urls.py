from django.urls import path

from .views import FacilitiesView, FacilityView, AddFacilityView, AddRatingView

urlpatterns = [
    path('', FacilitiesView.as_view(), name='facilities'),
    path('<int:pk>', FacilityView.as_view(), name='facility'),
    path('add/', AddFacilityView.as_view(), name='add_facility'),
    path('<int:facility_id>/add_rating/', AddRatingView.as_view(), name='add_rating'),
]
