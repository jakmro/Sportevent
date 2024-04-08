from django import forms

from .models import Facility, Rating


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = [
            'name',
            'description',
            'images',
            'location',
            'sport_type',
            'is_indoor',
            'contact_information'
        ]


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = [
            'rating',
            'comment'
        ]
