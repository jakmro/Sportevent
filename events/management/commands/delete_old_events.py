from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from events.models import Event


class Command(BaseCommand):
    help = 'Delete old events'

    def handle(self, *args, **options):
        now = timezone.now()
        threshold = now - timedelta(days=1)
        old_events = Event.objects.filter(end_datetime__lt=threshold, repeat_every_n_days=None)
        n = len(old_events)
        old_events.delete()
        self.stdout.write(f'Deleted {n} events')
