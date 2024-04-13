from django.forms import ModelForm
from .models import Facility, Rating


class FacilityForm(ModelForm):
    class Meta:
        model = Facility
        fields = [
            'name',
            'description',
            'image',
            'location',
            'sport_type',
            'is_indoor',
            'contact_information'
        ]


class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = [
            'rating',
            'comment'
        ]
