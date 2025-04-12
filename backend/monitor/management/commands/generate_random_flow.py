from django.core.management.base import BaseCommand
from monitor.models import FlowCalculation, ChannelSettings
from django.utils import timezone
import os
import random

class Command(BaseCommand):
    help = "Generate a realistic FlowCalculation record with smooth Pd variation"

    def handle(self, *args, **kwargs):
        try:
            settings = ChannelSettings.objects.first()
            if not settings:
                self.stdout.write(self.style.ERROR("❌ No ChannelSettings found."))
                return

            # File to keep track of last Pd value
            state_file = "/tmp/last_pd_value.txt"

            # Load last Pd value
            if os.path.exists(state_file):
                with open(state_file, "r") as f:
                    last_Pd = float(f.read())
            else:
                # Initial Pd around 9810 Pa (~1m water height)
                last_Pd = random.uniform(8000, 11000)

            # Simulate natural fluctuation
            variation = random.uniform(-200, 200)
            new_Pd = round(last_Pd + variation, 2)

            # Clamp between safe range (0.1m to 1.5m)
            min_Pd = round(settings.rho * settings.g * 0.1, 2)
            max_Pd = round(settings.rho * settings.g * 1.5, 2)
            new_Pd = max(min_Pd, min(max_Pd, new_Pd))

            # Save new Pd back to file
            with open(state_file, "w") as f:
                f.write(str(new_Pd))

            # Create FlowCalculation with Pd (h, Q, etc. will be calculated automatically)
            flow = FlowCalculation.objects.create(
                settings=settings,
                Pd=new_Pd,
                timestamp=timezone.now()
            )

            self.stdout.write(self.style.SUCCESS(
                f"✅ Created flow with Pd = {new_Pd} Pa at {flow.timestamp}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error: {str(e)}"))


# class Command(BaseCommand):
#     help = "Temporarily disabled: Generate a realistic FlowCalculation record"

#     def handle(self, *args, **kwargs):
#         self.stdout.write(self.style.WARNING("⏸ Flow generation is currently disabled. To re-enable, uncomment logic inside the command."))
#         pass