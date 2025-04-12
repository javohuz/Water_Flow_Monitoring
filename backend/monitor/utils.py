from django.utils import timezone
from django.db.models import Avg
from datetime import timedelta
from .models import (
    FlowCalculation,
    HourlyFlowSummary,
    WeeklyFlowSummary,
    MonthlyFlowSummary
)


def create_hourly_summary():
    now = timezone.now()
    hour_start = now.replace(minute=0, second=0, microsecond=0)
    hour_end = hour_start + timedelta(hours=1)

    flows = FlowCalculation.objects.filter(
        timestamp__gte=hour_start,
        timestamp__lt=hour_end,
        Pd__gt=0
    )

    if flows.exists():
        avg_Pd = flows.aggregate(avg_Pd=Avg('Pd'))['avg_Pd']
        settings = flows.first().settings

        HourlyFlowSummary.objects.update_or_create(
            timestamp=hour_start,
            defaults={
                'Pd': round(avg_Pd, 4),
                'settings': settings
            }
        )


def create_weekly_summary():
    now = timezone.now()
    week_start = now - timedelta(days=now.weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    week_end = week_start + timedelta(days=7)

    hourly_summaries = HourlyFlowSummary.objects.filter(
        timestamp__gte=week_start,
        timestamp__lt=week_end,
        Pd__gt=0
    )

    if hourly_summaries.exists():
        avg_Pd = hourly_summaries.aggregate(avg_Pd=Avg('Pd'))['avg_Pd']
        settings = hourly_summaries.first().settings

        WeeklyFlowSummary.objects.update_or_create(
            timestamp=week_start,
            defaults={
                'Pd': round(avg_Pd, 4),
                'settings': settings
            }
        )


def create_monthly_summary():
    now = timezone.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    if month_start.month == 12:
        next_month = month_start.replace(year=month_start.year + 1, month=1)
    else:
        next_month = month_start.replace(month=month_start.month + 1)

    weekly_summaries = WeeklyFlowSummary.objects.filter(
        timestamp__gte=month_start,
        timestamp__lt=next_month,
        Pd__gt=0
    )

    if weekly_summaries.exists():
        avg_Pd = weekly_summaries.aggregate(avg_Pd=Avg('Pd'))['avg_Pd']
        settings = weekly_summaries.first().settings

        MonthlyFlowSummary.objects.update_or_create(
            timestamp=month_start,
            defaults={
                'Pd': round(avg_Pd, 4),
                'settings': settings
            }
        )


# send telegram bot
import requests

TELEGRAM_TOKEN = "7869334590:AAFYOlGkogXUP67ENXus1ckWvJYFLtrjzts"
CHAT_IDS = ["853958315", "706057765"]  

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    for chat_id in CHAT_IDS:
        payload = {
            "chat_id": chat_id,
            "text": message
        }
        try:
            response = requests.post(url, data=payload)
            if response.status_code != 200:
                print(f"❌ Telegram error for {chat_id}:", response.text)
        except Exception as e:
            print(f"❌ Telegram exception for {chat_id}:", str(e))


# https://api.telegram.org/bot7869334590:AAFYOlGkogXUP67ENXus1ckWvJYFLtrjzts/getUpdates