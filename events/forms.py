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
            'date',
            'is_cyclic',
            'max_people_no',
            'min_people_no'
        ]
        widgets = {
            'date': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
        }

class EventRegistrationForm(ModelForm):
    class Meta:
        model = EventRegistration
        fields = []
