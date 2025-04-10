from django.core.management.base import BaseCommand
from monitor.models import FlowCalculation, ChannelSettings
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = "Generate hourly flow data for the past 3 months"

    def handle(self, *args, **kwargs):
        settings = ChannelSettings.objects.first()
        if not settings:
            self.stdout.write(self.style.ERROR("No ChannelSettings found."))
            return

        now = timezone.now()
        start_time = now - timedelta(days=90)
        total_hours = 90 * 24

        # Initial h (starting height)
        h = round(random.uniform(0.3, 0.7), 4)

        for i in range(total_hours):
            timestamp = start_time + timedelta(hours=i)

            # Add slow randomness to simulate real change
            h_change = random.uniform(-0.02, 0.02)
            h += h_change

            # Clamp to valid range
            h = max(0.1, min(h, 1.5))

            FlowCalculation.objects.create(
                settings=settings,
                h=round(h, 4),
                timestamp=timestamp
            )

            if i % 24 == 0:
                self.stdout.write(f"✅ Created {i} / {total_hours} hourly records...")

        self.stdout.write(self.style.SUCCESS("✅ Finished generating 3 months of hourly flow data."))
