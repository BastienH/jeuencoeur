from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from games.models import AnalyticsEvent


class Command(BaseCommand):
    help = 'Delete analytics events older than the specified number of days'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=90,
            help='Delete events older than this many days (default: 90)',
        )

    def handle(self, *args, **options):
        days = options['days']
        cutoff = timezone.now() - timedelta(days=days)
        deleted, _ = AnalyticsEvent.objects.filter(created_at__lt=cutoff).delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {deleted} analytics events older than {days} days.'))
