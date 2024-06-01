from django.db.models import Avg
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.conf import settings
from facilities.models import Facility, Rating


class MapView(TemplateView):
    template_name = 'maps/map.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.GOOGLE_API_KEY
        return context


def get_facilities_data(request):
    facilities = list(Facility.objects.values())
    for i, facility in enumerate(facilities):
        rating = Rating.objects.filter(facility_id=facility['id']).aggregate(Avg('rating'))
        if rating['rating__avg']:
            rounded_rating = round(rating['rating__avg'], 1)
        else:
            rounded_rating = 'No ratings'
        facilities[i]['rating'] = rounded_rating
    return JsonResponse(facilities, safe=False)
