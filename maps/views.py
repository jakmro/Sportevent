from django.views.generic import TemplateView
from django.conf import settings


class MapView(TemplateView):
    template_name = 'maps/map.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.GOOGLE_API_KEY
        return context
