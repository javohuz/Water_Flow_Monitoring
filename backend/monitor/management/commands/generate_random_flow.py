from django.core.management.base import BaseCommand
from monitor.models import FlowCalculation, ChannelSettings
from django.utils import timezone
import os
import random

# class Command(BaseCommand):
#     help = "Generate a realistic FlowCalculation record with smooth h variation"

#     def handle(self, *args, **kwargs):
#         try:
#             settings = ChannelSettings.objects.first()
#             if not settings:
#                 self.stdout.write(self.style.ERROR("No ChannelSettings found."))
#                 return

#             # File to keep track of last value
#             state_file = "/tmp/last_h_value.txt"

#             # Load last h value
#             if os.path.exists(state_file):
#                 with open(state_file, "r") as f:
#                     last_h = float(f.read())
#             else:
#                 last_h = random.uniform(0.5, 1.0)  # Starting point

#             # Smooth fluctuation logic
#             variation = random.uniform(-0.1, 0.1)
#             new_h = round(last_h + variation, 4)

#             # Clamp between 0.1 and 1.5 meters
#             new_h = max(0.1, min(1.5, new_h))

#             # Save new h back to file
#             with open(state_file, "w") as f:
#                 f.write(str(new_h))

#             # Create FlowCalculation record
#             flow = FlowCalculation.objects.create(
#                 settings=settings,
#                 h=new_h,
#                 timestamp=timezone.now()
#             )

#             self.stdout.write(self.style.SUCCESS(f"✅ Created flow with h = {new_h} at {flow.timestamp}"))

#         except Exception as e:
#             self.stdout.write(self.style.ERROR(f"❌ Error: {str(e)}"))


class Command(BaseCommand):
    help = "Temporarily disabled: Generate a realistic FlowCalculation record"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("⏸ Flow generation is currently disabled. To re-enable, uncomment logic inside the command."))
        pass