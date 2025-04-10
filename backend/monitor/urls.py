from django.urls import path
from .views import flow_data_view , hourly_data_view , weekly_data_view, monthly_data_view

urlpatterns = [
    path('', flow_data_view, name='flow_data'),
    path('hourly/', hourly_data_view, name='hourly_data'),
    path('weekly/', weekly_data_view, name='weekly_data'),
    path('monthly/', monthly_data_view, name='monthly_data'),
]
