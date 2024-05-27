from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.utils.translation import gettext
from events.models import Event, EventRegistration, Meeting
from .models import ChatMessage

def room(request, room_name):
    chat = ChatMessage.objects.get(id=room_name)
    event = chat.meeting.event
    registration = EventRegistration.objects.filter(event=event, user=request.user)
    if not registration:
        raise Http404(
            gettext("You are not registered on this event")
        )
    return render(request, "chat/room.html", {"room_name": room_name})
