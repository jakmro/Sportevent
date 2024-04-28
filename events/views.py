from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.utils.translation import gettext
from django.db.models import Q
from sqlite3 import IntegrityError
from .forms import EventForm, EventRegistrationForm
from .models import Event, EventRegistration


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

        try:
            context['registration'] = EventRegistration.objects.get(user_id=user_id, event_id=event_id)
        except EventRegistration.DoesNotExist:
            context['registration'] = None

        return context


class AddEventView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/add_event.html'
    success_url = reverse_lazy('events')

    def form_valid(self, form):
        form.instance.user = self.request.user
        start_datetime = form.cleaned_data['start_datetime']
        end_datetime = form.cleaned_data['end_datetime']

        if start_datetime > end_datetime:
            form.add_error('start_datetime', 'Start datetime must be less than or equal to End datetime.')
            return self.form_invalid(form)

        min_people_no = form.cleaned_data['min_people_no']
        max_people_no = form.cleaned_data['max_people_no']

        if min_people_no > max_people_no:
            form.add_error('min_people_no', 'Min people no must be less than or equal to Max people no.')
            return self.form_invalid(form)

        return super().form_valid(form)


class UpdateEventView(LoginRequiredMixin, UpdateView):
    model = Event
    fields = [
        'name',
        'facility',
        'description',
        'sport_type',
        'start_datetime',
        'end_datetime',
        'is_cyclic',
        'min_people_no',
        'max_people_no'
    ]
    template_name = 'events/update_event.html'

    def get_success_url(self):
        event_id = self.get_object().id
        return reverse_lazy('event', kwargs={'pk': event_id})

    def get_object(self, queryset=None):
        obj = super(UpdateEventView, self).get_object(queryset)
        if obj.user != self.request.user:
            raise Http404(
                gettext("It's not your event.")
            )
        return obj

    def form_valid(self, form):
        start_datetime = form.cleaned_data['start_datetime']
        end_datetime = form.cleaned_data['end_datetime']

        if start_datetime > end_datetime:
            form.add_error('start_datetime', 'Start datetime must be less than or equal to End datetime.')
            return self.form_invalid(form)

        min_people_no = form.cleaned_data['min_people_no']
        max_people_no = form.cleaned_data['max_people_no']

        if min_people_no > max_people_no:
            form.add_error('min_people_no', 'Min people no must be less than or equal to Max people no.')
            return self.form_invalid(form)

        return super().form_valid(form)


class DeleteEventView(LoginRequiredMixin, DeleteView):
    model = Event
    success_url = '/events'
    template_name = 'events/delete_event.html'

    def get_object(self, queryset=None):
        obj = super(DeleteEventView, self).get_object(queryset)
        if obj.user != self.request.user:
            raise Http404(
                gettext("It's not your event.")
            )
        return obj


class AddRegistrationView(LoginRequiredMixin, CreateView):
    model = EventRegistration
    form_class = EventRegistrationForm
    template_name = 'events/add_registration.html'

    def get_success_url(self):
        event_id = self.kwargs.get('event_id')
        return reverse_lazy('event', kwargs={'pk': event_id})

    def form_valid(self, form):
        event_id = self.kwargs.get('event_id')
        form.instance.event = Event.objects.get(id=event_id)
        form.instance.user = self.request.user

        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error(None, "You are already registered for this event.")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs.get('event_id')
        event = Event.objects.get(pk=event_id)
        context['event'] = event
        return context


class DeleteRegistrationView(LoginRequiredMixin, DeleteView):
    model = EventRegistration
    template_name = 'events/delete_registration.html'

    def __init__(self, *args, **kwargs):
        self.event_id = None
        super(DeleteRegistrationView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('event', kwargs={'pk': self.event_id})

    def get_object(self, queryset=None):
        obj = super(DeleteRegistrationView, self).get_object(queryset)
        if obj.user != self.request.user:
            raise Http404(
                gettext("It's not your event registration.")
            )
        # saving event_id for future use
        self.event_id = obj.event.id

        return obj
