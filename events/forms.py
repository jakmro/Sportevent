from django.forms import ModelForm, DateTimeInput
from .models import Event, EventRegistration


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = [
            'name',
            'facility',
            'description',
            'sport_type',
            'start_datetime',
            'end_datetime',
            'repeat_every_n_days',
            'min_people_no',
            'max_people_no'
        ]
        widgets = {
            'start_datetime': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_datetime': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
        }


class EventRegistrationForm(ModelForm):
    class Meta:
        model = EventRegistration
        fields = []
