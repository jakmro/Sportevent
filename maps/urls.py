from django.urls import path
from .views import (
    MapView,
    get_facilities_data
)

urlpatterns = [
    path('', MapView.as_view(), name='maps'),
    path('facilities_data/', get_facilities_data, name='get_facilities_data')
]
