from django import forms

from .models import Facility, OpenHours, Rating


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = [
            'name',
            'description',
            'images',
            'location',
            'sport_type',
            'capacity',
            'is_indoor',
            'contact_information'
        ]


class OpenHoursForm(forms.ModelForm):
    class Meta:
        model = OpenHours
        fields = [
            'user',
            'facility',
            'day',
            'open_time',
            'close_time'
        ]


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = [
            'user',
            'facility',
            'rating',
            'description'
        ]
