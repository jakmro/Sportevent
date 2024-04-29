from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from django.db.models import Avg, Q
from django.utils.translation import gettext
from django.db import IntegrityError

from events.models import Event
from .utils import geocode
from .forms import FacilityForm, RatingForm
from .models import Facility, Rating


class FacilitiesView(ListView):
    model = Facility
    template_name = 'facilities/facilities.html'
    context_object_name = 'facilities_list'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Facility.objects.all()
        if query:
            object_list = object_list.filter(
                Q(name__contains=query) |
                Q(description__contains=query) |
                Q(location__contains=query) |
                Q(sport_type__contains=query)
            )
        return object_list


class AddFacilityView(LoginRequiredMixin, CreateView):
    model = Facility
    form_class = FacilityForm
    template_name = 'facilities/add_facility.html'
    success_url = reverse_lazy('facilities')

    def form_valid(self, form):
        form.instance.user = self.request.user
        location = form.cleaned_data['location']
        latitude, longitude = geocode(location)

        if latitude is None and longitude is None:
            form.add_error('location', gettext('Invalid location.'))
            return self.form_invalid(form)

        form.instance.latitude = latitude
        form.instance.longitude = longitude

        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error('location', 'We already have an object in this location.')
            return self.form_invalid(form)


class FacilityView(DetailView):
    model = Facility
    template_name = 'facilities/facility.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ratings'] = Rating.objects.filter(facility=self.get_object().id)
        context['events'] = Event.objects.filter(facility=self.get_object().id)

        try:
            context['user_rating'] = Rating.objects.get(user=self.get_object().user.id)
        except Rating.DoesNotExist:
            context['user_rating'] = None

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

        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error(None, 'You can rate the same facility only once.')
            return self.form_invalid(form)


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
        'image',
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

    def form_valid(self, form):
        location = form.cleaned_data['location']
        latitude, longitude = geocode(location)

        if latitude is None and longitude is None:
            form.add_error('location', gettext('Invalid location.'))
            return self.form_invalid(form)

        form.instance.latitude = latitude
        form.instance.longitude = longitude

        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error('location', 'We already have an object in this location.')
            return self.form_invalid(form)


def get_facilities_data(request):
    facilities = list(Facility.objects.values())
    for i, facility in enumerate(facilities):
        rating = Rating.objects.filter(facility_id=facility['id']).aggregate(Avg('rating'))
        if rating['rating__avg']:
            rounded_rating = round(rating['rating__avg'], 1)
        else:
            rounded_rating = 'No ratings'
        facilities[i]['rating'] = rounded_rating
    return JsonResponse(facilities, safe=False)


class UpdateRatingView(LoginRequiredMixin, UpdateView):
    model = Rating
    fields = [
        'rating',
        'comment',
    ]
    template_name = 'facilities/update_rating.html'

    def get_success_url(self):
        facility_id = self.get_object().facility.id
        return reverse_lazy('facility', kwargs={'pk': facility_id})

    def get_object(self, queryset=None):
        obj = super(UpdateRatingView, self).get_object(queryset)
        if obj.user != self.request.user:
            raise Http404(
                gettext("It's not your rating.")
            )
        return obj


class DeleteRatingView(LoginRequiredMixin, DeleteView):
    model = Rating
    template_name = 'facilities/delete_rating.html'

    def __init__(self, *args, **kwargs):
        self.facility_id = None
        super(DeleteRatingView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('facility', kwargs={'pk': self.facility_id})

    def get_object(self, queryset=None):
        obj = super(DeleteRatingView, self).get_object(queryset)
        if obj.user != self.request.user:
            raise Http404(
                gettext("It's not your rating.")
            )
        # saving facility_id for future use
        self.facility_id = obj.facility.id

        return obj
