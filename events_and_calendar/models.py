from django.db import models
from django.conf import settings
from django.urls import reverse

class Event(models.Model):
    title = models.CharField(
        max_length=200, 
        verbose_name="Назва події"
    )
    description = models.TextField(
        verbose_name="Опис події", 
        blank=True
    )
    start_time = models.DateTimeField(
        verbose_name="Час початку"
    )
    end_time = models.DateTimeField(
        verbose_name="Час закінчення", 
        null=True, 
        blank=True
    )
    location = models.CharField(
        max_length=255, 
        verbose_name="Місце проведення", 
        blank=True
    )
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_events',
        verbose_name="Автор"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    class Meta:
        ordering = ['start_time']
        verbose_name = "Подія"
        verbose_name_plural = "Події"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('events_and_calendar:event_detail', kwargs={'pk': self.pk})