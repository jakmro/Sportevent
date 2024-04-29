from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from events.models import Event


class Command(BaseCommand):
    help = 'Delete old events'

    def handle(self, *args, **options):
        now = timezone.now()
        threshold = now - timedelta(days=1)
        Event.objects.filter(end_datetime__lt=threshold, is_cyclic=False).delete()
        self.stdout.write(f'Deleted old events')
