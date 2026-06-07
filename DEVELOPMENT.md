# Development Guide

## Project Architecture

### Backend Architecture
- **Framework**: Django 4.2
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Authentication**: Django's built-in User model and authentication system
- **ORM**: Django ORM for database operations

### Frontend Architecture
- **Template Engine**: Django Templates
- **CSS Framework**: Bootstrap 5
- **JavaScript**: Vanilla JS with Bootstrap's built-in interactions
- **QR Code**: qrcode.js library with Pillow for image generation

## Setup for Development

### 1. Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 3. Run Server
```bash
python manage.py runserver
```

## File Structure

```
d:\Python 2.0\Vrit.ly (v.2.0)/
│
├── urlshortener/                 # Main Django project
│   ├── __init__.py
│   ├── settings.py              # Django configuration
│   ├── urls.py                  # Main URL routing
│   ├── asgi.py                  # ASGI configuration
│   └── wsgi.py                  # WSGI configuration
│
├── shortener/                    # Main application
│   ├── migrations/              # Database migrations
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   │
│   ├── templates/               # HTML templates
│   │   └── shortener/
│   │       ├── base.html
│   │       ├── landing.html
│   │       ├── register.html
│   │       ├── login.html
│   │       ├── dashboard.html
│   │       ├── create.html
│   │       ├── url_detail.html
│   │       ├── edit.html
│   │       ├── delete_confirm.html
│   │       └── expired.html
│   │
│   ├── static/                  # Static files
│   │   ├── css/
│   │   └── js/
│   │
│   ├── __init__.py
│   ├── admin.py                 # Django admin configuration
│   ├── apps.py                  # App configuration
│   ├── models.py                # Database models
│   ├── views.py                 # View functions
│   ├── forms.py                 # Form definitions
│   ├── urls.py                  # App URL routing
│   ├── utils.py                 # Utility functions
│   └── tests.py                 # Unit tests
│
├── db.sqlite3                   # SQLite database
├── manage.py                    # Django CLI
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
├── QUICKSTART.md               # Quick start guide
├── DEVELOPMENT.md              # This file
└── .gitignore                  # Git ignore file
```

## Key Models

### ShortenedURL
```python
user = ForeignKey(User)           # URL owner
original_url = URLField()         # Long URL
short_key = CharField(unique=True) # Auto-generated code
custom_key = CharField(unique=True) # User custom code
click_count = PositiveIntegerField() # Click counter
created_at = DateTimeField()      # Creation timestamp
updated_at = DateTimeField()      # Update timestamp
expires_at = DateTimeField()      # Expiration date
is_active = BooleanField()        # Soft delete flag
```

### URLClickLog
```python
shortened_url = ForeignKey(ShortenedURL) # Related short URL
clicked_at = DateTimeField()      # Click timestamp
ip_address = GenericIPAddressField() # Client IP
user_agent = TextField()          # Browser info
```

## Views Overview

### Public Views
- `landing_page()` - Welcome page
- `register()` - User registration
- `login_view()` - User login
- `logout_view()` - User logout
- `redirect_to_url()` - Handle short URL redirects

### Authenticated Views
- `dashboard()` - User's URL dashboard
- `create_short_url()` - Create new shortened URL
- `url_detail()` - View URL details and analytics
- `edit_url()` - Edit shortened URL
- `delete_url()` - Delete shortened URL
- `get_qr_code()` - Retrieve QR code

## Forms

### RegisterForm
- Fields: username, email, password, password_confirm
- Validation: Password matching, email uniqueness

### LoginForm
- Fields: username, password
- Validation: User existence and password correctness

### ShortenURLForm
- Fields: original_url, expires_in_days
- Validation: Valid URL format

### CustomShortForm
- Fields: custom_key
- Validation: Uniqueness, minimum length (3 chars)

## URL Patterns

### App URLs (shortener/urls.py)
```
''                      → landing_page
'register/'            → register
'login/'               → login_view
'logout/'              → logout_view
'dashboard/'           → dashboard
'create/'              → create_short_url
'url/<id>/'            → url_detail
'url/<id>/edit/'       → edit_url
'url/<id>/delete/'     → delete_url
'url/<id>/qr/'         → get_qr_code
's/<short_code>/'      → redirect_to_url
```

## Base62 Encoding

Short URL generation uses Base62 encoding:
- Characters: 0-9, a-z, A-Z (62 total)
- Default length: 6 characters
- Combinations for 6 chars: 62^6 = ~56.8 billion
- Collision handling: Auto-regenerate if exists

Implementation in `utils.py`:
```python
BASE62_CHARS = string.digits + string.ascii_letters
def generate_short_key(length=6):
    while True:
        short_key = ''.join(random.choices(BASE62_CHARS, k=length))
        if not ShortenedURL.objects.filter(short_key=short_key).exists():
            return short_key
```

## QR Code Generation

Process:
1. Create QR code object with short URL
2. Generate PNG image using Pillow
3. Encode as Base64
4. Return as data URI for HTML embedding
5. Allow download as PNG file

Implementation in `views.py`:
```python
def generate_qr_code(short_url):
    qr = qrcode.QRCode(...)
    qr.add_data(short_url_full)
    img = qr.make_image()
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"
```

## Security Considerations

### CSRF Protection
- All forms include `{% csrf_token %}`
- CSRF middleware enabled in settings

### SQL Injection Prevention
- Django ORM prevents SQL injection
- Always use `.filter()` instead of raw queries

### Authentication
- Login required decorator on protected views
- User-specific access control
- Password hashing with PBKDF2

### URL Validation
- URLField validates HTTP/HTTPS URLs
- Prevents malicious URL creation

## Testing

### Running Tests
```bash
python manage.py test
```

### Test Coverage
```bash
coverage run --source='.' manage.py test
coverage report
```

### Creating Tests
```python
from django.test import TestCase
from django.contrib.auth.models import User
from .models import ShortenedURL

class ShortenedURLTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com', 'pass')
        
    def test_url_creation(self):
        url = ShortenedURL.objects.create(
            user=self.user,
            original_url='https://example.com',
            short_key='abc123'
        )
        self.assertEqual(url.short_key, 'abc123')
```

## Performance Optimization

### Database Optimization
- Add indexes on frequently searched fields
- Use `select_related()` for foreign keys
- Use `prefetch_related()` for reverse relations

```python
# In views.py
urls = request.user.shortened_urls.select_related('user').prefetch_related('click_logs')
```

### Caching Strategy
- Cache QR codes after generation
- Use memcached for click counts (optional)
- Implement database query caching

### Query Optimization
```python
# Good - Single query
short_url = ShortenedURL.objects.get(pk=1)

# Bad - Multiple queries
for url in ShortenedURL.objects.all():
    print(url.user.username)  # N+1 problem

# Good - Use select_related
urls = ShortenedURL.objects.select_related('user')
```

## Logging

### Enable Logging
```python
# In settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    },
}
```

### Using Logging
```python
import logging
logger = logging.getLogger(__name__)
logger.debug('Short URL created: %s', short_url.short_key)
```

## Deployment Checklist

- [ ] Set `DEBUG = False` in settings
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use environment variables for secrets
- [ ] Set up HTTPS/SSL certificate
- [ ] Configure static files collection
- [ ] Set up database backups
- [ ] Configure email backend
- [ ] Set up monitoring/logging
- [ ] Configure CORS if needed
- [ ] Test email functionality
- [ ] Set up CDN for static files
- [ ] Configure rate limiting

## Common Issues

### Migration Issues
```bash
# View migration status
python manage.py showmigrations

# Rollback migrations
python manage.py migrate shortener 0001

# Squash migrations (production)
python manage.py squashmigrations shortener
```

### Database Issues
```bash
# Reset database (development only)
rm db.sqlite3
python manage.py migrate

# Check database integrity
python manage.py dbshell
```

### Import Errors
```bash
# Ensure app is in INSTALLED_APPS
# Run migrate if models changed
python manage.py migrate
```

## IDE Setup

### VS Code
```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "[python]": {
        "editor.defaultFormatter": "ms-python.python",
        "editor.formatOnSave": true
    }
}
```

### PyCharm
- Mark `venv` as excluded
- Mark `static` as resource folder
- Configure Django support in settings

## Git Workflow

### Basic Git Commands
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <url>
git push -u origin main
```

### Typical Workflow
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
git add .
git commit -m "Add new feature"

# Push to remote
git push origin feature/new-feature

# Create pull request
# (on GitHub/GitLab)
```

## Code Style

### PEP 8 Compliance
```bash
# Check code style
flake8 shortener/

# Format code
black shortener/
```

### Django Best Practices
- Use model managers for queries
- Keep business logic in models
- Keep views thin
- Use signals sparingly
- Document complex code

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Best Practices](https://docs.djangoproject.com/en/stable/intro/contributing/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [QRCode Documentation](https://github.com/lincolnloop/python-qrcode)

---

**Happy Developing! 🚀**
