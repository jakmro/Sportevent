from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.utils.translation import gettext
from django.db.models import Q
from django.core.mail import send_mail
from ics import Calendar, Event as IcsEvent
from sqlite3 import IntegrityError
from .forms import EventForm, EventRegistrationForm
from .models import Event, EventRegistration, Meeting
from .helpers import validate_event_form, add_meetings
from accounts.mixins import EmailVerificationRequiredMixin


class EventsView(ListView):
    model = Event
    template_name = 'events/events.html'
    context_object_name = 'events_list'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Event.objects.all()
        if query:
            object_list = object_list.filter(
                Q(name__contains=query) |
                Q(description__contains=query) |
                Q(sport_type__contains=query)
            )
        return object_list


class EventView(DetailView):
    model = Event
    template_name = 'events/event.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.get_object().id
        user_id = self.request.user.id
        context['registrations'] = EventRegistration.objects.filter(event=event_id)

        try:
            context['registration'] = EventRegistration.objects.get(user_id=user_id, event_id=event_id)
        except EventRegistration.DoesNotExist:
            context['registration'] = None

        subscription_link = self.request.build_absolute_uri(reverse('event_calendar', kwargs={'event_id': event_id}))
        context['subscription_link'] = subscription_link

        return context


def event_calendar(request, event_id):
    event = Event.objects.get(id=event_id)
    meetings = Meeting.objects.filter(event=event)
    calendar = Calendar()
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
    response['Content-Disposition'] = 'attachment; filename="event_calendar.ics"'

    return response


class AddEventView(LoginRequiredMixin, EmailVerificationRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/add_event.html'
    success_url = reverse_lazy('events')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = validate_event_form(self, form)
        if response:
            return response
        response = super().form_valid(form)
        add_meetings(self, form)
        return response


class UpdateEventView(LoginRequiredMixin, EmailVerificationRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/update_event.html'

    def get_success_url(self):
        event_id = self.get_object().id
        return reverse_lazy('event', kwargs={'pk': event_id})

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404(
                gettext("It's not your event.")
            )
        return obj

    def form_valid(self, form):
        Meeting.objects.filter(event_id=self.get_object().id).delete()
        response = validate_event_form(self, form)
        if response:
            return response
        response = super().form_valid(form)
        add_meetings(self, form)
        return response


class DeleteEventView(LoginRequiredMixin, EmailVerificationRequiredMixin, DeleteView):
    model = Event
    success_url = '/events'
    template_name = 'events/delete_event.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404(
                gettext("It's not your event.")
            )
        return obj


class AddRegistrationView(LoginRequiredMixin, EmailVerificationRequiredMixin, CreateView):
    model = EventRegistration
    form_class = EventRegistrationForm
    template_name = 'events/add_registration.html'

    def get_success_url(self):
        event_id = self.kwargs.get('event_id')
        return reverse_lazy('event', kwargs={'pk': event_id})

    def form_valid(self, form):
        form.instance.user = self.request.user
        event_id = self.kwargs.get('event_id')
        event = Event.objects.get(id=event_id)
        form.instance.event = event

        event_meetings = Meeting.objects.filter(event_id=event_id)
        registrations = EventRegistration.objects.filter(user=self.request.user)
        event_ids = registrations.values_list('event_id', flat=True)
        meetings = Meeting.objects.filter(event_id__in=event_ids)

        for meeting in meetings:
            for event_meeting in event_meetings:
                if (meeting.start_datetime < event_meeting.end_datetime
                        and meeting.end_datetime > event_meeting.start_datetime):
                    form.add_error(
                        None,
                        'You are registered for an event that is taking place at the same time.'
                    )
                    return self.form_invalid(form)

        registrations_for_event = EventRegistration.objects.filter(event=event)
        if len(registrations_for_event) >= event.max_people_no:
            form.add_error(
                None,
                'Max people no of people has been reached.'
            )
            return self.form_invalid(form)

        try:
            host = event.user
            response = super().form_valid(form)
            send_mail(
                f'Someone joined your event',
                f'{self.request.user.username} joined your event {event.name}',
                None,
                [host.email]
            )
            return response
        except IntegrityError:
            form.add_error(None, 'You are already registered for this event.')
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs.get('event_id')
        event = Event.objects.get(pk=event_id)
        context['event'] = event
        return context


class DeleteRegistrationView(LoginRequiredMixin, EmailVerificationRequiredMixin, DeleteView):
    model = EventRegistration
    template_name = 'events/delete_registration.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_id = None

    def get_success_url(self):
        return reverse_lazy('event', kwargs={'pk': self.event_id})

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404(
                gettext("It's not your event registration.")
            )
        # saving event_id for future use
        self.event_id = obj.event.id

        return obj

    def form_valid(self, form):
        host = self.get_object().user
        event = self.get_object().event
        response = super().form_valid(form)
        send_mail(
            f'Someone has unregistered from your event',
            f'{self.request.user.username} has unregistered from {event.name}',
            None,
            [host.email]
        )
        return response
