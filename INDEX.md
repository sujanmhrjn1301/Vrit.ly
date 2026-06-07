# Project Index - URL Shortener Application

## 📑 Documentation Files

Start here to understand the project:

| File | Purpose | Read Time |
|------|---------|-----------|
| **[SETUP.md](SETUP.md)** | Complete setup instructions | 5 min |
| **[QUICKSTART.md](QUICKSTART.md)** | Quick 5-minute start guide | 3 min |
| **[README.md](README.md)** | Full project documentation | 15 min |
| **[FEATURES.md](FEATURES.md)** | Comprehensive features list | 10 min |
| **[DEVELOPMENT.md](DEVELOPMENT.md)** | Development guidelines | 20 min |
| **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | Project overview | 10 min |

## 🚀 Getting Started

### For First-Time Users
1. Read [SETUP.md](SETUP.md) - 5 minutes
2. Run: `pip install -r requirements.txt`
3. Run: `python manage.py migrate`
4. Run: `python manage.py runserver`
5. Visit: http://localhost:8000/

### For Developers
1. Read [DEVELOPMENT.md](DEVELOPMENT.md) - Understand architecture
2. Read [QUICKSTART.md](QUICKSTART.md) - Quick reference
3. Run tests: `python manage.py test shortener`
4. Start hacking!

## 📁 Project Structure

```
Project Root
│
├── 📚 Documentation
│   ├── SETUP.md                 ← Start here
│   ├── QUICKSTART.md
│   ├── README.md
│   ├── FEATURES.md
│   ├── DEVELOPMENT.md
│   ├── PROJECT_SUMMARY.md
│   └── INDEX.md                 ← You are here
│
├── 🐍 Django Project
│   ├── manage.py                ← Django CLI
│   ├── requirements.txt          ← Dependencies
│   ├── db.sqlite3               ← Database
│   │
│   ├── urlshortener/            ← Project settings
│   │   ├── settings.py          ← Configuration
│   │   ├── urls.py              ← Main URL routing
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   └── shortener/               ← Main application
│       ├── models.py            ← Database models
│       ├── views.py             ← View functions
│       ├── forms.py             ← Form definitions
│       ├── urls.py              ← App URL routing
│       ├── utils.py             ← Utility functions
│       ├── admin.py             ← Admin configuration
│       ├── tests.py             ← Unit tests (15 tests)
│       ├── apps.py
│       │
│       ├── migrations/
│       │   ├── 0001_initial.py
│       │   └── __init__.py
│       │
│       ├── templates/shortener/
│       │   ├── base.html        ← Base template
│       │   ├── landing.html     ← Landing page
│       │   ├── register.html    ← Registration
│       │   ├── login.html       ← Login page
│       │   ├── dashboard.html   ← User dashboard
│       │   ├── create.html      ← Create URL
│       │   ├── url_detail.html  ← URL details + QR
│       │   ├── edit.html        ← Edit URL
│       │   ├── delete_confirm.html
│       │   └── expired.html     ← Expired URL page
│       │
│       └── static/
│           ├── css/
│           └── js/
│
├── 🔧 Configuration
│   ├── .env.example              ← Environment template
│   └── .gitignore               ← Git ignore patterns
│
└── 📦 Other
    └── Prompt                   ← Original task
```

## 📊 Quick Stats

| Metric | Count |
|--------|-------|
| Python Files | 13 |
| HTML Templates | 9 |
| Documentation Files | 6 |
| Database Models | 2 |
| View Functions | 11 |
| Forms | 4 |
| URL Patterns | 11 |
| Unit Tests | 15 ✅ |
| Total Lines of Code | ~2,500 |
| Total Lines of Docs | ~3,000 |

## 🎯 Key Features

### User Authentication ✅
- Register, login, logout
- Session management
- Password security

### URL Shortening ✅
- Base62 encoding
- Auto-generated codes
- Custom codes
- 56+ billion combinations

### URL Management ✅
- Create, read, update, delete
- Expiration dates
- View all user URLs

### Analytics ✅
- Click tracking
- IP logging
- Statistics display

### QR Codes ✅
- Generate for short URLs
- Download as PNG
- Base64 embedded display

### Admin Interface ✅
- Manage users
- Manage URLs
- View analytics
- Advanced filtering

## 🧪 Testing

### Run Tests
```bash
python manage.py test shortener
```

### Test Results
- **Total Tests**: 15
- **Status**: ✅ All Passing
- **Coverage**: Core functionality

### Test Categories
- Model tests (4)
- View tests (7)
- Utils tests (2)
- Integration tests (2)

## 🔑 Key Files Explained

### Models (`shortener/models.py`)
Defines two database models:
- **ShortenedURL** - Main model for shortened URLs
- **URLClickLog** - Tracks clicks and analytics

### Views (`shortener/views.py`)
11 view functions handling:
- Authentication (register, login, logout)
- URL management (create, read, update, delete)
- Redirect and click tracking
- QR code generation

### Forms (`shortener/forms.py`)
4 forms for:
- User registration
- User login
- URL shortening
- Custom short code

### Templates (`shortener/templates/`)
9 HTML templates using Bootstrap 5:
- Base layout with navbar
- Landing page
- Authentication pages
- Dashboard
- CRUD operations
- Error pages

### Utils (`shortener/utils.py`)
Helper functions:
- Base62 short key generation
- Client IP detection
- Collision prevention

## 🔗 URL Routes

### Public Routes
```
/                    → Landing page
/register/          → User registration
/login/             → User login
/logout/            → User logout
/s/<short_code>/    → Redirect to original URL
```

### Authenticated Routes
```
/dashboard/         → View all URLs
/create/            → Create URL form
/url/<id>/          → View URL details
/url/<id>/edit/     → Edit URL
/url/<id>/delete/   → Delete URL
/url/<id>/qr/       → Get QR code (JSON)
```

### Admin
```
/admin/             → Django admin panel
```

## 💾 Database Models

### ShortenedURL
```python
user            → ForeignKey(User)
original_url    → URLField(max_length=2000)
short_key       → CharField(unique=True)
custom_key      → CharField(unique=True, optional)
click_count     → PositiveIntegerField
created_at      → DateTimeField(auto)
updated_at      → DateTimeField(auto)
expires_at      → DateTimeField(optional)
is_active       → BooleanField(default=True)
```

### URLClickLog
```python
shortened_url   → ForeignKey(ShortenedURL)
clicked_at      → DateTimeField(auto)
ip_address      → GenericIPAddressField
user_agent      → TextField
```

## 🛠️ Development Commands

### Setup
```bash
pip install -r requirements.txt      # Install dependencies
python manage.py migrate             # Apply migrations
python manage.py createsuperuser     # Create admin user
```

### Running
```bash
python manage.py runserver           # Start dev server
python manage.py test shortener      # Run tests
python manage.py shell               # Interactive shell
```

### Database
```bash
python manage.py makemigrations      # Create migrations
python manage.py migrate             # Apply migrations
python manage.py sqlmigrate shortener 0001  # Preview SQL
python manage.py dbshell            # Database shell
```

### Admin
```bash
python manage.py createsuperuser    # Create admin
python manage.py changepassword <user>  # Reset password
```

## 📖 Reading Guide

### For Users
1. [SETUP.md](SETUP.md) - Install and run
2. [QUICKSTART.md](QUICKSTART.md) - First steps
3. [README.md](README.md) - Feature guide

### For Developers
1. [DEVELOPMENT.md](DEVELOPMENT.md) - Architecture
2. Review `shortener/models.py` - Database schema
3. Review `shortener/views.py` - Business logic
4. Review `shortener/templates/` - UI
5. Run tests to understand flow

### For DevOps/Deployment
1. [DEVELOPMENT.md](DEVELOPMENT.md) - Production checklist
2. [SETUP.md](SETUP.md) - Deployment section
3. Review `urlshortener/settings.py` - Configuration

### For Security Review
1. [FEATURES.md](FEATURES.md) - Security section
2. Review `shortener/views.py` - Auth decorators
3. Review `shortener/forms.py` - Validation
4. Review Django middleware in `settings.py`

## 🚀 Quick Commands

```bash
# Setup (5 minutes)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Test everything
python manage.py test shortener

# Create admin account
python manage.py createsuperuser

# Reset database
rm db.sqlite3
python manage.py migrate

# Run specific test
python manage.py test shortener.tests.ShortenedURLModelTest
```

## 📞 Common Questions

### Q: How do I start?
A: Read [SETUP.md](SETUP.md) and run 3 commands.

### Q: Where's the documentation?
A: See the Documentation Files section above.

### Q: How do I extend it?
A: See [DEVELOPMENT.md](DEVELOPMENT.md).

### Q: Are there tests?
A: Yes! 15 tests, all passing. Run: `python manage.py test shortener`

### Q: Can I deploy this?
A: Yes! See [DEVELOPMENT.md](DEVELOPMENT.md) deployment section.

### Q: How do I customize?
A: Edit templates in `shortener/templates/` or models in `shortener/models.py`

## ✅ Verification Checklist

- [ ] Read SETUP.md
- [ ] Installed dependencies
- [ ] Ran migrations
- [ ] Started server
- [ ] Visited http://localhost:8000/
- [ ] Created account
- [ ] Created short URL
- [ ] Generated QR code
- [ ] Tested redirect
- [ ] Viewed dashboard
- [ ] Ran tests (15 passing)
- [ ] Read README.md

## 🎓 Learning Objectives

This project teaches:
- Django project structure
- Database modeling
- User authentication
- Form handling
- URL routing
- Template rendering
- Click tracking
- QR code generation
- Testing in Django
- Admin interface
- Production deployment

## 📝 Additional Resources

### Django Documentation
- [Django Official Docs](https://docs.djangoproject.com/)
- [Django Models](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [Django Views](https://docs.djangoproject.com/en/stable/topics/http/views/)
- [Django Forms](https://docs.djangoproject.com/en/stable/topics/forms/)

### QR Code
- [qrcode Library](https://github.com/lincolnloop/python-qrcode)
- [Pillow Documentation](https://pillow.readthedocs.io/)

### Bootstrap
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)
- [Bootstrap Components](https://getbootstrap.com/docs/5.0/components/)

## 🎉 You're Ready!

Everything is set up and documented. Start with [SETUP.md](SETUP.md) and enjoy building!

---

**Last Updated**: June 7, 2026  
**Project Status**: ✅ COMPLETE  
**Test Status**: ✅ 15/15 PASSING  
**Documentation**: ✅ COMPLETE
