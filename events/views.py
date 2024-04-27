from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from django.utils.translation import gettext

from .forms import EventForm
from .models import Event


class EventsView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/events.html'
    context_object_name = 'events_list'

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
    success_url = reverse_lazy('events')

    def get_object(self, queryset=None):
        obj = super(UpdateEventView, self).get_object(queryset)
        if obj.user != self.request.user:
            raise Http404(
                gettext("It's not your event.")
            )
        return obj