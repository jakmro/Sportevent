from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from .forms import FacilityForm, OpenHoursForm, RatingForm
from .models import Facility, OpenHours, Rating


class FacilitiesView(ListView):
    model = Facility
    template_name = "facilities/facilities.html"


class AddFacilityView(CreateView):
    model = Facility
    form_class = FacilityForm
    template_name = "facilities/add_facility.html"
    success_url = reverse_lazy("facilities")


class AddOpenHoursView(CreateView):
    model = OpenHours
    form_class = OpenHoursForm
    template_name = "facilities/add_open_hours.html"
    success_url = reverse_lazy("facilities")


class AddRatingView(CreateView):
    model = Rating
    form_class = RatingForm
    template_name = "facilities/add_rating.html"
    success_url = reverse_lazy("facilities")
