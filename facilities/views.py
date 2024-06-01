from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.db.models import Avg, Q, FloatField, Count
from django.db.models.functions import Round
from django.utils.translation import gettext
from django.db import IntegrityError
from ics import Calendar, Event as IcsEvent
from events.models import Event, Meeting
from .utils import geocode
from .forms import FacilityForm, RatingForm
from .models import Facility, Rating
from accounts.mixins import EmailVerificationRequiredMixin


class FacilityView(DetailView):
    model = Facility
    template_name = 'facilities/facility.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ratings'] = Rating.objects.filter(facility=self.get_object().id)
        context['events'] = Event.objects.filter(facility=self.get_object().id)

        try:
            context['user_rating'] = Rating.objects.get(user=self.request.user.id, facility=self.get_object().id)
        except Rating.DoesNotExist:
            context['user_rating'] = None

        subscription_link = self.request.build_absolute_uri(
            reverse('facility_calendar', kwargs={'pk': self.get_object().id}))
        context['subscription_link'] = subscription_link

        return context


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
        object_list = object_list.annotate(avg_rating=Round(Avg('rating__rating'), 1, output_field=FloatField()))
        object_list = object_list.annotate(total_comments=Count('rating__comment'))
        return object_list


class AddFacilityView(LoginRequiredMixin, EmailVerificationRequiredMixin, CreateView):
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


class UpdateFacilityView(LoginRequiredMixin, EmailVerificationRequiredMixin, UpdateView):
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
        obj = super().get_object(queryset)
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


class DeleteFacilityView(LoginRequiredMixin, EmailVerificationRequiredMixin, DeleteView):
    model = Facility
    success_url = '/facilities'
    template_name = 'facilities/delete_facility.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404(
                gettext("You don't own this object")
            )
        return obj


def facility_calendar(request, pk):
    facility = Facility.objects.get(pk=pk)
    events = Event.objects.filter(facility=facility)
    calendar = Calendar()
    for event in events:
        meetings = Meeting.objects.filter(event=event)
        for meeting in meetings:
            ics_event = IcsEvent()
            ics_event.name = event.name
            ics_event.begin = meeting.start_datetime
            ics_event.end = meeting.end_datetime
            ics_event.description = event.description
            ics_event.location = event.facility.name
            ics_event.categories = event.sport_type
            calendar.events.add(ics_event)

    response = HttpResponse(str(calendar), content_type='text/calendar')
    response['Content-Disposition'] = 'attachment; filename="facility_calendar.ics"'

    return response


class AddRatingView(LoginRequiredMixin, EmailVerificationRequiredMixin, CreateView):
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


class UpdateRatingView(LoginRequiredMixin, EmailVerificationRequiredMixin, UpdateView):
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
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404(
                gettext("It's not your rating.")
            )
        return obj


class DeleteRatingView(LoginRequiredMixin, EmailVerificationRequiredMixin, DeleteView):
    model = Rating
    template_name = 'facilities/delete_rating.html'

    def __init__(self, *args, **kwargs):
        self.facility_id = None
        super().__init__(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('facility', kwargs={'pk': self.facility_id})

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404(
                gettext("It's not your rating.")
            )
        # saving facility_id for future use
        self.facility_id = obj.facility.id

        return obj
