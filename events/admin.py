from django.contrib import admin
from .models import Event, Meeting, EventRegistration

admin.site.register(Event)
admin.site.register(Meeting)
admin.site.register(EventRegistration)
