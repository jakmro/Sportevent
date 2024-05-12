from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from events.models import Event, Meeting


def get_end_datetime(event):
    end_datetime = event.end_datetime
    repeat_every_n_days = event.repeat_every_n_days
    meeting_count = event.meeting_count
    if repeat_every_n_days:
        end_datetime += meeting_count * timedelta(days=repeat_every_n_days)
    return end_datetime


class Command(BaseCommand):
    help = 'Delete old events'

    def handle(self, *args, **options):
        now = timezone.now()
        threshold = now - timedelta(days=1)

        events = Event.objects.all()
        old_events_ids = [event.id for event in events if get_end_datetime(event) < threshold]
        old_meetings = Meeting.objects.filter(end_datetime__lt=threshold)

        old_events_count = len(old_events_ids)
        old_meetings_count = len(old_meetings)

        Event.objects.filter(id__in=old_events_ids).delete()
        old_meetings.delete()

        self.stdout.write(f'Deleted {old_events_count} events and {old_meetings_count} meetings')
