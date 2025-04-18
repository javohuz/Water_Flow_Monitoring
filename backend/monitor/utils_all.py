# If you want to upadte for all time datas witho those codes lets use this one steps
#
# python manage.py shell

# from monitor.utils_all import create_all_hourly_summaries, create_all_weekly_summaries, create_all_monthly_summaries

# create_all_hourly_summaries()
# create_all_weekly_summaries()
# create_all_monthly_summaries()


from django.utils import timezone
from django.db.models import Avg
from datetime import timedelta
from .models import (
    FlowCalculation,
    HourlyFlowSummary,
    WeeklyFlowSummary,
    MonthlyFlowSummary,
)

def create_all_hourly_summaries():
    first_entry = FlowCalculation.objects.order_by('timestamp').first()
    last_entry = FlowCalculation.objects.order_by('-timestamp').first()

    if not first_entry or not last_entry:
        print("No FlowCalculation data available.")
        return

    current_time = first_entry.timestamp.replace(minute=0, second=0, microsecond=0)
    end_time = last_entry.timestamp.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

    while current_time < end_time:
        next_hour = current_time + timedelta(hours=1)
        flows = FlowCalculation.objects.filter(timestamp__gte=current_time, timestamp__lt=next_hour)

        if flows.exists():
            avg_Pd = flows.aggregate(avg_Pd=Avg('Pd'))['avg_Pd']
            settings = flows.first().settings

            HourlyFlowSummary.objects.update_or_create(
                timestamp=current_time,
                defaults={'Pd': round(avg_Pd, 4), 'settings': settings}
            )

        current_time = next_hour

    print("✅ Hourly summaries generated from FlowCalculation.")


def create_all_weekly_summaries():
    first_entry = HourlyFlowSummary.objects.order_by('timestamp').first()
    last_entry = HourlyFlowSummary.objects.order_by('-timestamp').first()

    if not first_entry or not last_entry:
        print("No HourlyFlowSummary data available.")
        return

    current_time = first_entry.timestamp - timedelta(days=first_entry.timestamp.weekday())
    current_time = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
    end_time = last_entry.timestamp.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=7)

    while current_time < end_time:
        next_week = current_time + timedelta(days=7)
        flows = HourlyFlowSummary.objects.filter(timestamp__gte=current_time, timestamp__lt=next_week)

        if flows.exists():
            avg_Pd = flows.aggregate(avg_Pd=Avg('Pd'))['avg_Pd']
            settings = flows.first().settings

            WeeklyFlowSummary.objects.update_or_create(
                timestamp=current_time,
                defaults={'Pd': round(avg_Pd, 4), 'settings': settings}
            )

        current_time = next_week

    print("✅ Weekly summaries generated from HourlyFlowSummary.")


def create_all_monthly_summaries():
    first_entry = WeeklyFlowSummary.objects.order_by('timestamp').first()
    last_entry = WeeklyFlowSummary.objects.order_by('-timestamp').first()

    if not first_entry or not last_entry:
        print("No WeeklyFlowSummary data available.")
        return

    current_time = first_entry.timestamp.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_time = (last_entry.timestamp.replace(day=28) + timedelta(days=4)).replace(day=1)

    while current_time < end_time:
        if current_time.month == 12:
            next_month = current_time.replace(year=current_time.year + 1, month=1)
        else:
            next_month = current_time.replace(month=current_time.month + 1)

        flows = WeeklyFlowSummary.objects.filter(timestamp__gte=current_time, timestamp__lt=next_month)

        if flows.exists():
            avg_Pd = flows.aggregate(avg_Pd=Avg('Pd'))['avg_Pd']
            settings = flows.first().settings

            MonthlyFlowSummary.objects.update_or_create(
                timestamp=current_time,
                defaults={'Pd': round(avg_Pd, 4), 'settings': settings}
            )

        current_time = next_month

    print("✅ Monthly summaries generated from WeeklyFlowSummary.")
