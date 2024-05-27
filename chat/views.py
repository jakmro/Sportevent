from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext
from events.models import EventRegistration, Event

def room(request, uidb64):
    room_name = urlsafe_base64_decode(uidb64).decode()
    event = Event.objects.get(id=room_name)
    registration = EventRegistration.objects.filter(event=event, user=request.user)
    if not registration:
        raise Http404(
            gettext("You are not registered on this event")
        )
    return render(request, "chat/room.html", {"room_name": room_name})
