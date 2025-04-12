from django.core.management.base import BaseCommand
from monitor.models import FlowCalculation, ChannelSettings
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = "🧪 Generate hourly flow data for the past 3 months using Pd (pressure)."

    def handle(self, *args, **kwargs):
        settings = ChannelSettings.objects.first()
        if not settings:
            self.stdout.write(self.style.ERROR("❌ No ChannelSettings found."))
            return

        # Remove all previous flow data
        FlowCalculation.objects.all().delete()
        self.stdout.write(self.style.WARNING("🗑️ Old flow records deleted."))

        now = timezone.now()
        start_time = now - timedelta(days=90)
        total_hours = 90 * 24

        # Initial Pd = rho * g * h
        initial_h = round(random.uniform(0.3, 0.7), 4)
        Pd = round(settings.rho * settings.g * initial_h, 2)

        for i in range(total_hours):
            timestamp = start_time + timedelta(hours=i)

            # Simulate natural fluctuation in Pd
            Pd_change = random.uniform(-100, 100)
            Pd += Pd_change

            # Clamp Pd (0.1m to 1.5m)
            min_Pd = round(settings.rho * settings.g * 0.1, 2)
            max_Pd = round(settings.rho * settings.g * 1.5, 2)
            Pd = max(min_Pd, min(Pd, max_Pd))

            FlowCalculation.objects.create(
                settings=settings,
                Pd=Pd,
                timestamp=timestamp
            )

            if i % 24 == 0:
                self.stdout.write(f"📦 Created {i} / {total_hours} hourly records...")

        self.stdout.write(self.style.SUCCESS("✅ Finished generating 3 months of hourly flow data."))
