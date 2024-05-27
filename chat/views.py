from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext
from django.utils import timezone
from events.models import EventRegistration, Event, Meeting
from datetime import timedelta

def room(request, uidb64):
    room_name = urlsafe_base64_decode(uidb64).decode()
    event = Event.objects.get(id=room_name)
    registration = EventRegistration.objects.filter(event=event, user=request.user)
    if not registration:
        raise Http404(
            gettext("You are not registered for this event")
        )
    now = timezone.now()
    meeting = Meeting.objects.filter(event=event).first()
    if now + timedelta(days=1) < meeting.start_datetime:
        raise Http404(
            gettext("Chat for this event has not started yet")
        )
    return render(request, "chat/room.html", {"room_name": room_name})
