from django.db import models
import math
from django.utils import timezone
from django.utils.timezone import localtime
from ckeditor.fields import RichTextField


class ChannelSettings(models.Model):
    name = models.CharField("Nom", max_length=100, default='Default Settings')

    n = models.FloatField("G'adir budurlik koyfitsienti n", default=0.013)
    b = models.FloatField("Kanal eni b (m)", default=1.0)
    alpha = models.FloatField("Yon devor burchagi α (gradus)", default=45.0)
    S = models.FloatField("Gidravlik qiyalik S", default=0.001)
    rho = models.FloatField("Zichlik ρ (kg/m³)", default=1000.0)
    g = models.FloatField("Erkin tushushi tezlanishi g (m/s²)", default=9.81)

    min_height = models.FloatField("Minimal suv balandligi (h)", default=0.3)
    max_height = models.FloatField("Maksimal suv balandligi (h)", default=1.2)

    image = models.ImageField("Kanal rasmi", upload_to="channel_images/", blank=True, null=True)
    description = RichTextField("Tavsif (HTML)", blank=True, null=True)

    def __str__(self):
        return self.name


class FlowCalculation(models.Model):
    settings = models.ForeignKey(ChannelSettings, on_delete=models.CASCADE, verbose_name="Kanal sozlamalari")
    Pd = models.FloatField("Gidrostatik bosim Pd (Pa)", help_text="Sensor orqali o‘lchanadi")

    h = models.FloatField("Hisoblangan suv balandligi h (m)", blank=True, null=True)
    A = models.FloatField("Yuza A (m²)", blank=True, null=True)
    P = models.FloatField("Perimetr P (m)", blank=True, null=True)
    R = models.FloatField("Gidravlik radius R (m)", blank=True, null=True)
    V = models.FloatField("Oqim tezligi V (m/s)", blank=True, null=True)
    Q = models.FloatField("Suv sarfi Q (m³/s)", blank=True, null=True)

    timestamp = models.DateTimeField("O‘lchov vaqti", default=timezone.now)

    class Meta:
        verbose_name = "Real vaqtdagi oqim"
        verbose_name_plural = "Real vaqtdagi oqimlar"
        ordering = ['-timestamp']

    def save(self, *args, **kwargs):
        if self.Pd is not None and self.settings:
            rho, g = self.settings.rho, self.settings.g
            self.h = round(self.Pd / (rho * g), 4)

            alpha_rad = math.radians(self.settings.alpha)
            self.A = round(self.h * (self.settings.b + 2 * self.h * math.tan(alpha_rad)), 4)
            self.P = round(self.settings.b + 2 * self.h / math.cos(alpha_rad), 4)
            self.R = round(self.A / self.P, 4)
            self.V = round((1 / self.settings.n) * (self.R ** (2 / 3)) * (self.settings.S ** 0.5), 4)
            self.Q = round(self.A * self.V, 4)

            from .utils import send_telegram_message
            if self.h < self.settings.min_height:
                send_telegram_message(f"⚠️ Ogohlantirish! Suv sathi juda past:\nh = {self.h} m\nQ = {self.Q} m³/s")
            elif self.h > self.settings.max_height:
                send_telegram_message(f"🚨 Diqqat! Suv sathi juda yuqori:\nh = {self.h} m\nQ = {self.Q} m³/s")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Oqim vaqti: {localtime(self.timestamp).strftime('%Y/%m/%d | %H:%M')}"


class BaseSummaryModel(models.Model):
    timestamp = models.DateTimeField()
    Pd = models.FloatField("Gidrostatik bosim Pd (Pa)", null=True, blank=True)
    h = models.FloatField("Hisoblangan h (m)", null=True, blank=True)

    A = models.FloatField("A (m²)", null=True, blank=True)
    P = models.FloatField("P (m)", null=True, blank=True)
    R = models.FloatField("R (m)", null=True, blank=True)
    V = models.FloatField("V (m/s)", null=True, blank=True)
    Q = models.FloatField("Q (m³/s)", null=True, blank=True)

    settings = models.ForeignKey(
        ChannelSettings,
        on_delete=models.CASCADE,
        verbose_name="Kanal sozlamalari",
        null=True,
        blank=True
    )

    class Meta:
        abstract = True

    def calculate_values(self):
        if self.Pd is not None and self.settings:
            rho, g = self.settings.rho, self.settings.g
            self.h = round(self.Pd / (rho * g), 4)

            alpha_rad = math.radians(self.settings.alpha)
            self.A = round(self.h * (self.settings.b + 2 * self.h * math.tan(alpha_rad)), 4)
            self.P = round(self.settings.b + 2 * self.h / math.cos(alpha_rad), 4)
            self.R = round(self.A / self.P, 4)
            self.V = round((1 / self.settings.n) * (self.R ** (2 / 3)) * (self.settings.S ** 0.5), 4)
            self.Q = round(self.A * self.V, 4)

    def save(self, *args, **kwargs):
        self.calculate_values()
        super().save(*args, **kwargs)



class HourlyFlowSummary(BaseSummaryModel):
    class Meta:
        verbose_name = "Soatlik oqim"
        verbose_name_plural = "Soatlik oqimlar"
        ordering = ['-timestamp']

    def __str__(self):
        return f"Soatlik o‘rtacha oqim: {self.timestamp.strftime('%Y/%m/%d | %H:00')}"


class WeeklyFlowSummary(BaseSummaryModel):
    class Meta:
        verbose_name = "Haftalik oqim"
        verbose_name_plural = "Haftalik oqimlar"
        ordering = ['-timestamp']

    def __str__(self):
        return f"Hafta boshidagi oqim: {self.timestamp.strftime('%Y/%m/%d')}"


class MonthlyFlowSummary(BaseSummaryModel):
    class Meta:
        verbose_name = "Oylik oqim"
        verbose_name_plural = "Oylik oqimlar"
        ordering = ['-timestamp']

    def __str__(self):
        return f"Oy boshidagi oqim: {self.timestamp.strftime('%Y/%m')}"
