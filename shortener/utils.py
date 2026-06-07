import string
import random
from .models import ShortenedURL

BASE62_CHARS = string.digits + string.ascii_letters

def generate_short_key(length=6):
    while True:
        short_key = ''.join(random.choices(BASE62_CHARS, k=length))
        if not ShortenedURL.objects.filter(short_key=short_key).exists():
            return short_key

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
