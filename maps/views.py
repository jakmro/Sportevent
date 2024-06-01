from django.db.models import Avg
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.conf import settings
from facilities.models import Facility, Rating
from events.models import Event, Meeting


class MapFacilitiesView(TemplateView):
    template_name = 'maps/map_facilities.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.GOOGLE_API_KEY
        return context


class MapEventsView(TemplateView):
    template_name = 'maps/map_events.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.GOOGLE_API_KEY
        return context


def get_facilities_data(request):
    facilities = Facility.objects.values()

    for i, facility in enumerate(facilities):
        rating = Rating.objects.filter(facility_id=facility['id']).aggregate(Avg('rating'))
        if rating['rating__avg']:
            rounded_rating = round(rating['rating__avg'], 1)
        else:
            rounded_rating = 'No ratings'
        facilities[i]['rating'] = rounded_rating

    facilities = list(facilities)
    return JsonResponse(facilities, safe=False)


def get_meetings_data(request):
    meetings = Meeting.objects.values()

    first_meetings = {}

    for i in range(len(meetings)):
        event = Event.objects.get(id=meetings[i]['event_id'])
        facility = Facility.objects.get(id=event.facility_id)

        meetings[i]['event_id'] = event.id
        meetings[i]['name'] = event.name
        meetings[i]['description'] = event.description
        meetings[i]['location'] = facility.location
        meetings[i]['latitude'] = facility.latitude
        meetings[i]['longitude'] = facility.longitude

        coordinates = (facility.latitude, facility.longitude)

        if coordinates in first_meetings:
            first_meetings[coordinates] = min(
                first_meetings[coordinates],
                meetings[i],
                key=lambda meeting: meeting['start_datetime']
            )
        else:
            first_meetings[coordinates] = meetings[i]

    for meeting in first_meetings.values():
        meeting['start_datetime'] = meeting['start_datetime'].strftime('%H:%M %d-%m-%Y')
        meeting['end_datetime'] = meeting['end_datetime'].strftime('%H:%M %d-%m-%Y')

    first_meetings = list(first_meetings.values())
    return JsonResponse(first_meetings, safe=False)
