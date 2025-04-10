from django.db import models
import math
from django.utils import timezone
from django.utils.timezone import localtime
from django.db.models import Avg
from ckeditor.fields import RichTextField

class ChannelSettings(models.Model):
    name = models.CharField("Nom", max_length=100, default='Default Settings')

    n = models.FloatField("Qo‘polilik koeffitsienti n", default=0.013)
    b = models.FloatField("Kanal eni b (m)", default=1.0)
    alpha = models.FloatField("Yon devor burchagi α (gradus)", default=45.0)
    S = models.FloatField("Gidravlik qiyalik S", default=0.001)
    rho = models.FloatField("Zichlik ρ (kg/m³)", default=1000.0)
    g = models.FloatField("Gravitatsiya g (m/s²)", default=9.81)
    Pd = models.FloatField("Bosim Pd (Pa)", default=9810.0)

    min_height = models.FloatField("Minimal suv balandligi (h)", default=0.3)
    max_height = models.FloatField("Maksimal suv balandligi (h)", default=1.2)

    image = models.ImageField("Kanal rasmi", upload_to="channel_images/", blank=True, null=True)
    description = RichTextField("Tavsif (HTML)", blank=True, null=True)
    
    def __str__(self):
        return self.name


class FlowCalculation(models.Model):
    settings = models.ForeignKey(
        ChannelSettings,
        on_delete=models.CASCADE,
        verbose_name="Kanal sozlamalari"
    )
    h = models.FloatField("Suv balandligi h (m)", help_text="Suv sathi metrda")

    A = models.FloatField("Yuza A (m²)", blank=True, null=True)
    P = models.FloatField("Perimetr P (m)", blank=True, null=True)
    R = models.FloatField("Gidravlik radius R (m)", blank=True, null=True)
    V = models.FloatField("Oqim tezligi V (m/s)", blank=True, null=True)
    Q = models.FloatField("Suv sarfi Q (m³/s)", blank=True, null=True)

    timestamp = models.DateTimeField(
        "O‘lchov vaqti",
        default=timezone.now,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Real vaqtdagi oqim"
        verbose_name_plural = "Real vaqtdagi oqimlar"
        ordering = ['-timestamp']

    def save(self, *args, **kwargs):
        if self.h is not None and self.settings:
            alpha_rad = math.radians(self.settings.alpha)
            self.A = round(self.h * (self.settings.b + 2 * self.h * math.tan(alpha_rad)), 4)
            self.P = round(self.settings.b + 2 * self.h / math.cos(alpha_rad), 4)
            self.R = round(self.A / self.P, 4)
            self.V = round((1 / self.settings.n) * (self.R ** (2 / 3)) * (self.settings.S ** 0.5), 4)
            self.Q = round(self.A * self.V, 4)

            from .utils import send_telegram_message
            
            if self.h < self.settings.min_height:
                send_telegram_message(
                    f"⚠️ Ogohlantirish! Suv sathi juda past:\n"
                    f"h = {self.h} m\n"
                    f"Q = {self.Q} m³/s"
                )
            elif self.h > self.settings.max_height:
                send_telegram_message(
                    f"🚨 Diqqat! Suv sathi juda yuqori:\n"
                    f"h = {self.h} m\n"
                    f"Q = {self.Q} m³/s"
                )


        super().save(*args, **kwargs)


    def __str__(self):
        local_time = localtime(self.timestamp)
        return f"Oqim vaqti: {local_time.strftime('%Y/%m/%d | %H:%M')}"


class HourlyFlowSummary(models.Model):
    timestamp = models.DateTimeField("Soat bo‘yicha vaqt")  # e.g. 2025-04-06 17:00
    h = models.FloatField("O‘rtacha h (m)", null=True, blank=True)
    A = models.FloatField("A (m²)", null=True, blank=True)
    P = models.FloatField("P (m)", null=True, blank=True)
    R = models.FloatField("R (m)", null=True, blank=True)
    V = models.FloatField("V (m/s)", null=True, blank=True)
    Q = models.FloatField("Q (m³/s)", null=True, blank=True)
    settings = models.ForeignKey(ChannelSettings, on_delete=models.CASCADE, verbose_name="Kanal sozlamalari", null=True, blank=True)

    class Meta:
        verbose_name = "Soatlik oqim"
        verbose_name_plural = "Soatlik oqimlar"
        ordering = ['-timestamp']

    def save(self, *args, **kwargs):
        if self.h is not None and self.settings:
            alpha_rad = math.radians(self.settings.alpha)

            self.A = round(self.h * (self.settings.b + 2 * self.h * math.tan(alpha_rad)), 4)
            self.P = round(self.settings.b + 2 * self.h / math.cos(alpha_rad), 4)
            self.R = round(self.A / self.P, 4)
            self.V = round((1 / self.settings.n) * (self.R ** (2 / 3)) * (self.settings.S ** 0.5), 4)
            self.Q = round(self.A * self.V, 4)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Soatlik o‘rtacha oqim: {self.timestamp.strftime('%Y/%m/%d | %H:00')}"


class WeeklyFlowSummary(models.Model):
    timestamp = models.DateTimeField("Haftalik vaqt (boshi)")  # Start of the week
    h = models.FloatField("O‘rtacha h (m)", null=True, blank=True)
    A = models.FloatField("A (m²)", null=True, blank=True)
    P = models.FloatField("P (m)", null=True, blank=True)
    R = models.FloatField("R (m)", null=True, blank=True)
    V = models.FloatField("V (m/s)", null=True, blank=True)
    Q = models.FloatField("Q (m³/s)", null=True, blank=True)
    settings = models.ForeignKey(ChannelSettings, on_delete=models.CASCADE, verbose_name="Kanal sozlamalari", null=True, blank=True)

    class Meta:
        verbose_name = "Haftalik oqim"
        verbose_name_plural = "Haftalik oqimlar"
        ordering = ['-timestamp']

    def save(self, *args, **kwargs):
        if self.h is not None and self.settings:
            alpha_rad = math.radians(self.settings.alpha)
            self.A = round(self.h * (self.settings.b + 2 * self.h * math.tan(alpha_rad)), 4)
            self.P = round(self.settings.b + 2 * self.h / math.cos(alpha_rad), 4)
            self.R = round(self.A / self.P, 4)
            self.V = round((1 / self.settings.n) * (self.R ** (2 / 3)) * (self.settings.S ** 0.5), 4)
            self.Q = round(self.A * self.V, 4)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Hafta boshidagi oqim: {self.timestamp.strftime('%Y/%m/%d')}"


class MonthlyFlowSummary(models.Model):
    timestamp = models.DateTimeField("Oylik vaqt (boshi)")
    h = models.FloatField("O‘rtacha h (m)", null=True, blank=True)
    A = models.FloatField("A (m²)", null=True, blank=True)
    P = models.FloatField("P (m)", null=True, blank=True)
    R = models.FloatField("R (m)", null=True, blank=True)
    V = models.FloatField("V (m/s)", null=True, blank=True)
    Q = models.FloatField("Q (m³/s)", null=True, blank=True)
    settings = models.ForeignKey(ChannelSettings, on_delete=models.CASCADE, verbose_name="Kanal sozlamalari", null=True, blank=True)

    class Meta:
        verbose_name = "Oylik oqim"
        verbose_name_plural = "Oylik oqimlar"
        ordering = ['-timestamp']

    def save(self, *args, **kwargs):
        if self.h is not None and self.settings:
            alpha_rad = math.radians(self.settings.alpha)
            self.A = round(self.h * (self.settings.b + 2 * self.h * math.tan(alpha_rad)), 4)
            self.P = round(self.settings.b + 2 * self.h / math.cos(alpha_rad), 4)
            self.R = round(self.A / self.P, 4)
            self.V = round((1 / self.settings.n) * (self.R ** (2 / 3)) * (self.settings.S ** 0.5), 4)
            self.Q = round(self.A * self.V, 4)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Oy boshidagi oqim: {self.timestamp.strftime('%Y/%m')}"
