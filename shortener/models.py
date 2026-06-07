from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import string
import random
from datetime import timedelta

class ShortenedURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shortened_urls', null=True, blank=True)
    original_url = models.URLField(max_length=2000)
    short_key = models.CharField(max_length=20, unique=True, db_index=True)
    custom_key = models.CharField(max_length=20, unique=True, null=True, blank=True, db_index=True)
    click_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Shortened URLs"

    def __str__(self):
        return f"{self.short_key} -> {self.original_url[:50]}"

    def get_short_code(self):
        return self.custom_key or self.short_key

    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False

    def increment_clicks(self):
        self.click_count += 1
        self.save(update_fields=['click_count'])


class URLClickLog(models.Model):
    shortened_url = models.ForeignKey(ShortenedURL, on_delete=models.CASCADE, related_name='click_logs')
    clicked_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ['-clicked_at']

    def __str__(self):
        return f"Click on {self.shortened_url.short_key} at {self.clicked_at}"
