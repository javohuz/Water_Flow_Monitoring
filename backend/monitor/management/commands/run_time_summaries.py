from django.core.management.base import BaseCommand
from monitor.utils import create_hourly_summary, create_weekly_summary, create_monthly_summary

class Command(BaseCommand):
    help = "Automatically creates hourly, weekly, and monthly flow summaries"

    def handle(self, *args, **kwargs):
        create_hourly_summary()
        create_weekly_summary()
        create_monthly_summary()
        self.stdout.write(self.style.SUCCESS("✅ Time summaries updated successfully"))
