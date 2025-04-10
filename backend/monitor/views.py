from django.shortcuts import render
from .models import ChannelSettings, FlowCalculation , HourlyFlowSummary , WeeklyFlowSummary, MonthlyFlowSummary

def flow_data_view(request):
    flows = FlowCalculation.objects.order_by('-timestamp')[:20]
    settings = ChannelSettings.objects.first()  
    return render(request, 'monitor.html', {
        'flows': flows,
        'settings': settings
    })

def hourly_data_view(request):
    hourly_flows = HourlyFlowSummary.objects.order_by('-timestamp')[:24]
    return render(request, 'monitor_hourly.html', {'hourly_flows': hourly_flows})

def weekly_data_view(request):
    weekly_flows = WeeklyFlowSummary.objects.order_by('-timestamp')[:12]
    return render(request, 'monitor_weekly.html', {'weekly_flows': weekly_flows})

def monthly_data_view(request):
    monthly_flows = MonthlyFlowSummary.objects.order_by('-timestamp')[:12]
    return render(request, 'monitor_monthly.html', {'monthly_flows': monthly_flows})