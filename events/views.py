from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.utils.translation import gettext
from django.db.models import Q

from .forms import EventForm
from .models import Event


class EventsView(LoginRequiredMixin, ListView):
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
        return context

class AddEventView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/add_event.html'
    success_url = reverse_lazy('events')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class UpdateEventView(LoginRequiredMixin, UpdateView):
    model = Event
    fields = [
        'name',
        'description',
        'sport_type',
        'date',
        'max_people_no',
        'min_people_no',
        'is_cyclic'
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

class DeleteEventView(LoginRequiredMixin, DeleteView):
    model = Event
    success_url = '/events'
    template_name = 'events/delete_event.html'

    def get_object(self, queryset=None):
        obj = super(DeleteEventView, self).get_object(queryset)
        if obj.user != self.request.user:
            raise Http404(
                gettext("You don't own this event")
            )
        return obj