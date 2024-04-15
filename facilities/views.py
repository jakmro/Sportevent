from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from django.conf import settings
from django.db.models import Avg
from django.utils.translation import gettext
import requests
import json
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

    def form_valid(self, form):
        form.instance.user = self.request.user

        location = form.cleaned_data['location']
        location_url_format = location.replace(' ', '+')

        res = requests.get(
            f'https://maps.googleapis.com/maps/api/geocode/json?address={location_url_format}&key={settings.GOOGLE_API_KEY}'
        )
        response = json.loads(res.text)

        latitude = response['results'][0]['geometry']['location']['lat']
        longitude = response['results'][0]['geometry']['location']['lng']

        form.instance.latitude = latitude
        form.instance.longitude = longitude

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

    def get_success_url(self):
        facility_id = self.kwargs.get('facility_id')
        return reverse_lazy('facility', kwargs={'pk': facility_id})

    def form_valid(self, form):
        facility_id = self.kwargs.get('facility_id')
        form.instance.facility = Facility.objects.get(id=facility_id)
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeleteFacilityView(LoginRequiredMixin, DeleteView):
    model = Facility
    success_url = '/facilities'
    template_name = 'facilities/delete_facility.html'

    def get_object(self, queryset=None):
        obj = super(DeleteFacilityView, self).get_object(queryset)
        if obj.user != self.request.user:
            raise Http404(
                gettext("You don't own this object")
            )
        return obj


class UpdateFacilityView(LoginRequiredMixin, UpdateView):
    model = Facility
    fields = [
        'name',
        'description',
        'location',
        'sport_type',
        'is_indoor',
        'contact_information'
    ]
    template_name = 'facilities/update_facility.html'

    def get_success_url(self):
        facility_id = self.kwargs.get('pk')
        return reverse_lazy('facility', kwargs={'pk': facility_id})

    def get_object(self, queryset=None):
        obj = super(UpdateFacilityView, self).get_object(queryset)
        if obj.user != self.request.user:
            raise Http404(
                gettext("You don't own this object")
            )
        return obj


def get_facilities_data(request):
    facilities = list(Facility.objects.values())
    for i, facility in enumerate(facilities):
        rating = Rating.objects.filter(facility_id=facility['id']).aggregate(Avg('rating'))
        if rating['rating__avg']:
            rounded_rating = round(rating['rating__avg'], 1)
        else:
            rounded_rating = "No ratings"
        facilities[i]['rating'] = rounded_rating
    return JsonResponse(facilities, safe=False)
