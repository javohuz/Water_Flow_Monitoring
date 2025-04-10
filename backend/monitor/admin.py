from django.contrib import admin
from .models import ChannelSettings, FlowCalculation , HourlyFlowSummary ,  WeeklyFlowSummary, MonthlyFlowSummary

@admin.register(ChannelSettings)
class ChannelSettingsAdmin(admin.ModelAdmin):
    list_display = ("name", "n", "b", "alpha")
    fieldsets = (
        ("Asosiy parametrlar", {
            "fields": ("name", "n", "b", "alpha", "S", "rho", "g", "Pd" ,'min_height', 'max_height' , 'description' , 'image')
        }),
    )


@admin.register(FlowCalculation)
class FlowCalculationAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "h", "Q", "V")
    readonly_fields = ("A", "P", "R", "V", "Q")  # Auto-calculated
    fieldsets = (
        ("Kiritiladigan ma'lumot", {
            "fields": ("settings", "h", "timestamp")
        }),
        ("Hisoblangan natijalar", {
            "fields": ("A", "P", "R", "V", "Q")
        }),
    )


@admin.register(HourlyFlowSummary)
class HourlyFlowSummaryAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "h", "Q", "V")
    readonly_fields = ("A", "P", "R", "V", "Q")  # Auto-calculated
    fieldsets = (
        ("Soatlik ma'lumot", {
            "fields": ("timestamp", "settings", "h")
        }),
        ("Hisoblangan natijalar", {
            "fields": ("A", "P", "R", "V", "Q")
        }),
    )



@admin.register(WeeklyFlowSummary)
class WeeklyFlowSummaryAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "h", "Q", "V")
    readonly_fields = ("A", "P", "R", "V", "Q")
    fieldsets = (
        ("Haftalik ma'lumot", {
            "fields": ("timestamp", "settings", "h")
        }),
        ("Hisoblangan qiymatlar", {
            "fields": ("A", "P", "R", "V", "Q")
        }),
    )

@admin.register(MonthlyFlowSummary)
class MonthlyFlowSummaryAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "h", "Q", "V")
    readonly_fields = ("A", "P", "R", "V", "Q")
    fieldsets = (
        ("Oylik ma'lumot", {
            "fields": ("timestamp", "settings", "h")
        }),
        ("Hisoblangan qiymatlar", {
            "fields": ("A", "P", "R", "V", "Q")
        }),
    )