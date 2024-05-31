from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from datetime import timedelta
from events.models import Meeting, EventRegistration

class Command(BaseCommand):
    help = 'Notify registered users about upcoming events'

    def handle(self, *args, **options):
        now = timezone.now()
        threshold = now + timedelta(days=1)

        upcoming_meetings = Meeting.objects.filter(start_datetime__lt=threshold, notification_sent=False)
        events = upcoming_meetings.values_list('event', flat=True)
        registrations = EventRegistration.objects.filter(event__in=events, user__email_verified=True)

        for registration in registrations:
            user = registration.user
            event = registration.event
            location = event.facility.location
            uidb64 = urlsafe_base64_encode(force_bytes(event.id))
            chat_link = self.request.build_absolute_uri(reverse('room', kwargs={'uidb64': uidb64}))
            send_mail(
                'Upcoming event',
                f'You have an upcoming event {event.name} in {location} at {event.start_datetime}.',
                f'Here is a link to chat for this event {chat_link}',
                None,
                [user.email]
            )

        upcoming_meetings.update(notification_sent=True)

        email_count = registrations.count()
        self.stdout.write(f'Number of emails sent: {email_count}')
