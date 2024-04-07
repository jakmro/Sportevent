from django.contrib import admin
from .models import Facility, OpenHours, Rating

admin.site.register(Facility)
admin.site.register(OpenHours)
admin.site.register(Rating)
