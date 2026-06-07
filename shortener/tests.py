from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import ShortenedURL, URLClickLog
from .utils import generate_short_key

class ShortenedURLModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_url_creation(self):
        url = ShortenedURL.objects.create(
            user=self.user,
            original_url='https://example.com',
            short_key='abc123'
        )
        self.assertEqual(url.short_key, 'abc123')
        self.assertEqual(url.click_count, 0)
        self.assertFalse(url.is_expired())

    def test_get_short_code_auto(self):
        url = ShortenedURL.objects.create(
            user=self.user,
            original_url='https://example.com',
            short_key='abc123'
        )
        self.assertEqual(url.get_short_code(), 'abc123')

    def test_get_short_code_custom(self):
        url = ShortenedURL.objects.create(
            user=self.user,
            original_url='https://example.com',
            short_key='abc123',
            custom_key='custom'
        )
        self.assertEqual(url.get_short_code(), 'custom')

    def test_increment_clicks(self):
        url = ShortenedURL.objects.create(
            user=self.user,
            original_url='https://example.com',
            short_key='abc123'
        )
        url.increment_clicks()
        url.refresh_from_db()
        self.assertEqual(url.click_count, 1)

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_landing_page(self):
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shortener/landing.html')

    def test_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shortener/register.html')

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shortener/login.html')

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(response.url.startswith('/login/'))

    def test_dashboard_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shortener/dashboard.html')

    def test_create_url_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('create_url'), {
            'original_url': 'https://example.com',
            'expires_in_days': ''
        })
        self.assertEqual(response.status_code, 302)  # Redirect to detail page
        self.assertEqual(ShortenedURL.objects.count(), 1)

    def test_redirect_to_url(self):
        url = ShortenedURL.objects.create(
            user=self.user,
            original_url='https://example.com',
            short_key='abc123'
        )
        response = self.client.get(reverse('redirect_url', args=['abc123']))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'https://example.com')

    def test_redirect_to_url_with_custom_key(self):
        url = ShortenedURL.objects.create(
            user=self.user,
            original_url='https://example.com',
            short_key='abc123',
            custom_key='custom'
        )
        response = self.client.get(reverse('redirect_url', args=['custom']))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'https://example.com')

    def test_click_logging(self):
        url = ShortenedURL.objects.create(
            user=self.user,
            original_url='https://example.com',
            short_key='abc123'
        )
        self.client.get(reverse('redirect_url', args=['abc123']))
        url.refresh_from_db()
        self.assertEqual(url.click_count, 1)
        self.assertEqual(URLClickLog.objects.count(), 1)

class UtilsTest(TestCase):
    def test_generate_short_key_uniqueness(self):
        key1 = generate_short_key()
        key2 = generate_short_key()
        self.assertNotEqual(key1, key2)

    def test_generate_short_key_length(self):
        key = generate_short_key()
        self.assertEqual(len(key), 6)
