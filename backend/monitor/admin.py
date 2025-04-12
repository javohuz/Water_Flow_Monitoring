from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources

from .models import (
    ChannelSettings,
    FlowCalculation,
    HourlyFlowSummary,
    WeeklyFlowSummary,
    MonthlyFlowSummary
)

# ========== RESOURCES ==========

class ChannelSettingsResource(resources.ModelResource):
    class Meta:
        model = ChannelSettings

class FlowCalculationResource(resources.ModelResource):
    class Meta:
        model = FlowCalculation

class HourlyFlowSummaryResource(resources.ModelResource):
    class Meta:
        model = HourlyFlowSummary

class WeeklyFlowSummaryResource(resources.ModelResource):
    class Meta:
        model = WeeklyFlowSummary

class MonthlyFlowSummaryResource(resources.ModelResource):
    class Meta:
        model = MonthlyFlowSummary

# ========== ADMINS ==========

@admin.register(ChannelSettings)
class ChannelSettingsAdmin(ImportExportModelAdmin):
    resource_class = ChannelSettingsResource
    list_display = ("name", "n", "b", "alpha")
    fieldsets = (
        ("Asosiy parametrlar", {
            "fields": ("name", "n", "b", "alpha", "S", "rho", "g", "min_height", "max_height", "description", "image")
        }),
    )


@admin.register(FlowCalculation)
class FlowCalculationAdmin(ImportExportModelAdmin):
    resource_class = FlowCalculationResource
    list_display = ("timestamp", "Pd", "h", "Q", "V")
    readonly_fields = ("h", "A", "P", "R", "V", "Q")
    fieldsets = (
        ("Sensor ma'lumotlari", {
            "fields": ("settings", "Pd", "timestamp")
        }),
        ("Hisoblangan natijalar", {
            "fields": ("h", "A", "P", "R", "V", "Q")
        }),
    )


@admin.register(HourlyFlowSummary)
class HourlyFlowSummaryAdmin(ImportExportModelAdmin):
    resource_class = HourlyFlowSummaryResource
    list_display = ("timestamp", "Pd", "h", "Q", "V")
    readonly_fields = ("h", "A", "P", "R", "V", "Q")
    fieldsets = (
        ("Soatlik ma'lumot", {
            "fields": ("timestamp", "settings", "Pd")
        }),
        ("Hisoblangan natijalar", {
            "fields": ("h", "A", "P", "R", "V", "Q")
        }),
    )


@admin.register(WeeklyFlowSummary)
class WeeklyFlowSummaryAdmin(ImportExportModelAdmin):
    resource_class = WeeklyFlowSummaryResource
    list_display = ("timestamp", "Pd", "h", "Q", "V")
    readonly_fields = ("h", "A", "P", "R", "V", "Q")
    fieldsets = (
        ("Haftalik ma'lumot", {
            "fields": ("timestamp", "settings", "Pd")
        }),
        ("Hisoblangan qiymatlar", {
            "fields": ("h", "A", "P", "R", "V", "Q")
        }),
    )


@admin.register(MonthlyFlowSummary)
class MonthlyFlowSummaryAdmin(ImportExportModelAdmin):
    resource_class = MonthlyFlowSummaryResource
    list_display = ("timestamp", "Pd", "h", "Q", "V")
    readonly_fields = ("h", "A", "P", "R", "V", "Q")
    fieldsets = (
        ("Oylik ma'lumot", {
            "fields": ("timestamp", "settings", "Pd")
        }),
        ("Hisoblangan qiymatlar", {
            "fields": ("h", "A", "P", "R", "V", "Q")
        }),
    )
