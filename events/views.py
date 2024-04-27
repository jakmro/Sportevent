from django.views.generic import ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Event


class EventsView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/events.html'
    context_object_name = 'events_list'
