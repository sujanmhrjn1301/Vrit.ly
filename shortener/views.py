from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Q
import string
import random
import qrcode
from io import BytesIO
import base64

from .models import ShortenedURL, URLClickLog
from .forms import ShortenURLForm, RegisterForm, LoginForm, CustomShortForm
from .utils import generate_short_key, get_client_ip

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    short_url = None
    if request.method == 'POST':
        form = ShortenURLForm(request.POST)
        if form.is_valid():
            original_url = form.cleaned_data['original_url']
            expiration_date = form.cleaned_data.get('expiration_date')

            short_key = generate_short_key()
            expires_at = None
            if expiration_date:
                expires_at = timezone.make_aware(
                    timezone.datetime.combine(expiration_date, timezone.datetime.max.time())
                )

            short_url = ShortenedURL.objects.create(
                user=request.user if request.user.is_authenticated else None,
                original_url=original_url,
                short_key=short_key,
                expires_at=expires_at
            )
    else:
        form = ShortenURLForm()

    context = {
        'form': form,
        'short_url': short_url
    }
    return render(request, 'shortener/landing.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'shortener/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                form.add_error(None, 'Invalid credentials')
    else:
        form = LoginForm()

    return render(request, 'shortener/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('landing')

@login_required(login_url='login')
def dashboard(request):
    urls = request.user.shortened_urls.filter(is_active=True).order_by('-created_at')
    return render(request, 'shortener/dashboard.html', {'urls': urls})

@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def create_short_url(request):
    if request.method == 'POST':
        form = ShortenURLForm(request.POST)
        if form.is_valid():
            original_url = form.cleaned_data['original_url']
            expiration_date = form.cleaned_data.get('expiration_date')

            short_key = generate_short_key()
            expires_at = None
            if expiration_date:
                expires_at = timezone.make_aware(
                    timezone.datetime.combine(expiration_date, timezone.datetime.max.time())
                )

            short_url = ShortenedURL.objects.create(
                user=request.user,
                original_url=original_url,
                short_key=short_key,
                expires_at=expires_at
            )

            return redirect('url_detail', pk=short_url.pk)
    else:
        form = ShortenURLForm()

    return render(request, 'shortener/create.html', {'form': form})

def url_detail_public(request, pk):
    short_url = get_object_or_404(ShortenedURL, pk=pk)

    if short_url.user and short_url.user != request.user and request.user.is_authenticated:
        return redirect('landing')

    qr_code_url = generate_qr_code(short_url)
    short_url_full = request.build_absolute_uri(f'/s/{short_url.get_short_code()}/')
    form = None

    if request.user.is_authenticated and (short_url.user == request.user or not short_url.user):
        if request.method == 'POST':
            form = CustomShortForm(request.POST, instance=short_url)
            if form.is_valid():
                if not short_url.user:
                    short_url.user = request.user
                form.save()
                return redirect('url_detail', pk=short_url.pk)
        else:
            form = CustomShortForm(instance=short_url)

    return render(request, 'shortener/url_detail_public.html', {
        'short_url': short_url,
        'form': form,
        'qr_code': qr_code_url,
        'short_url_full': short_url_full,
        'is_owner': request.user.is_authenticated and (short_url.user == request.user or not short_url.user)
    })

@login_required(login_url='login')
def url_detail(request, pk):
    short_url = get_object_or_404(ShortenedURL, pk=pk, user=request.user)

    if request.method == 'POST':
        form = CustomShortForm(request.POST, instance=short_url)
        if form.is_valid():
            form.save()
            return redirect('url_detail', pk=short_url.pk)
    else:
        form = CustomShortForm(instance=short_url)

    qr_code_url = generate_qr_code(short_url)
    short_url_full = request.build_absolute_uri(f'/s/{short_url.get_short_code()}/')

    return render(request, 'shortener/url_detail.html', {
        'short_url': short_url,
        'form': form,
        'qr_code': qr_code_url,
        'short_url_full': short_url_full
    })

@login_required(login_url='login')
def edit_url(request, pk):
    short_url = get_object_or_404(ShortenedURL, pk=pk, user=request.user)

    if request.method == 'POST':
        short_url.original_url = request.POST.get('original_url', short_url.original_url)
        short_url.save()
        return redirect('url_detail', pk=short_url.pk)

    return render(request, 'shortener/edit.html', {'short_url': short_url})

@login_required(login_url='login')
def delete_url(request, pk):
    short_url = get_object_or_404(ShortenedURL, pk=pk, user=request.user)

    if request.method == 'POST':
        short_url.is_active = False
        short_url.save()
        return redirect('dashboard')

    return render(request, 'shortener/delete_confirm.html', {'short_url': short_url})

def redirect_to_url(request, short_code):
    short_url = get_object_or_404(
        ShortenedURL,
        Q(short_key=short_code) | Q(custom_key=short_code),
        is_active=True
    )

    if short_url.is_expired():
        return render(request, 'shortener/expired.html')

    URLClickLog.objects.create(
        shortened_url=short_url,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    short_url.increment_clicks()

    return redirect(short_url.original_url)

@login_required(login_url='login')
def get_qr_code(request, pk):
    short_url = get_object_or_404(ShortenedURL, pk=pk, user=request.user)
    qr_code_url = generate_qr_code(short_url)
    return JsonResponse({'qr_code': qr_code_url})

def generate_qr_code(short_url):
    short_url_full = f"http://localhost:8000/s/{short_url.get_short_code()}/"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(short_url_full)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{qr_code_base64}"
