from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import EventForm
from .models import Event, Facility


class EventsView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/events.html'
    context_object_name = 'events_list'

class AddEventView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/add_event.html'
    success_url = reverse_lazy('facilities')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
