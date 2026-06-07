from django.contrib import admin
from .models import ShortenedURL, URLClickLog

@admin.register(ShortenedURL)
class ShortenedURLAdmin(admin.ModelAdmin):
    list_display = ('get_short_code', 'user', 'original_url', 'click_count', 'created_at', 'is_active')
    list_filter = ('created_at', 'is_active', 'expires_at')
    search_fields = ('short_key', 'custom_key', 'original_url', 'user__username')
    readonly_fields = ('short_key', 'created_at', 'updated_at')

    def get_short_code(self, obj):
        return obj.get_short_code()
    get_short_code.short_description = 'Short Code'

@admin.register(URLClickLog)
class URLClickLogAdmin(admin.ModelAdmin):
    list_display = ('shortened_url', 'clicked_at', 'ip_address')
    list_filter = ('clicked_at',)
    search_fields = ('shortened_url__short_key', 'ip_address')
    readonly_fields = ('clicked_at',)
