from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import FacilityForm, RatingForm
from .models import Facility, Rating


class FacilitiesView(ListView):
    model = Facility
    template_name = 'facilities/facilities.html'


class AddFacilityView(LoginRequiredMixin, CreateView):
    model = Facility
    form_class = FacilityForm
    template_name = 'facilities/add_facility.html'
    success_url = reverse_lazy('facilities')
    login_url = '/accounts/login/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class FacilityView(DetailView):
    model = Facility
    template_name = 'facilities/facility.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ratings'] = Rating.objects.filter(facility=self.get_object().id)
        return context


class AddRatingView(LoginRequiredMixin, CreateView):
    model = Rating
    form_class = RatingForm
    template_name = 'facilities/add_rating.html'
    login_url = '/accounts/login/'

    def get_success_url(self):
        facility_id = self.kwargs.get('facility_id')
        return reverse_lazy('facility', kwargs={'pk': facility_id})

    def form_valid(self, form):
        facility_id = self.kwargs.get('facility_id')
        form.instance.facility = Facility.objects.get(id=facility_id)
        form.instance.user = self.request.user
        return super().form_valid(form)

class DeleteFacilityView(DeleteView):
    model = Facility
    success_url = '/facilities'
    template_name = 'facilities/delete_facility.html'

class UpdateFacilityView(UpdateView):
    model = Facility
    fields = [
        'name',
        'description',
        'location',
        'sport_type',
        'is_indoor',
        'contact_information'
    ]
    success_url = '/facilities'
    template_name = 'facilities/update_facility.html'