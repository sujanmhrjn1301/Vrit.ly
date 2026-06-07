# Complete Setup Instructions

## Initial Setup

### Step 1: Check Python Installation
```bash
python --version  # Should be 3.8 or higher
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Setup Database
```bash
python manage.py migrate
```

### Step 4: Create Admin User (Optional but Recommended)
```bash
python manage.py createsuperuser
# Follow prompts to create username, email, password
```

### Step 5: Run Development Server
```bash
python manage.py runserver
```

## Accessing the Application

Once the server is running:

### Main Application
- **URL**: http://localhost:8000/
- **Description**: Public landing page with authentication options

### Admin Panel
- **URL**: http://localhost:8000/admin/
- **Login**: Use superuser credentials created in Step 4
- **Features**: Manage users, URLs, and click logs

## First-Time User Walkthrough

### 1. Create an Account
```
1. Click "Create Account" on landing page
2. Enter username, email, and password
3. Click "Create Account"
```

### 2. Create Your First Short URL
```
1. Click "Create New URL" or "Create URL" in navigation
2. Enter a long URL (e.g., https://docs.djangoproject.com/)
3. Optionally set expiration (e.g., 30 days)
4. Click "Create Short URL"
```

### 3. View Details
```
1. You'll be redirected to the URL details page
2. See your short URL
3. View QR code
4. Copy the short URL to clipboard
```

### 4. Share or Customize
```
1. Click "View" to see details again
2. Use "Edit Custom Code" to personalize
3. Click "Edit" to change the original URL
4. Monitor click statistics
```

## Environment Configuration

### Create .env File (Optional)
```bash
# Copy from template
copy .env.example .env
```

### Edit .env for Your Setup
```
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
SHORT_URL_PREFIX=http://localhost:8000/s/
```

## Virtual Environment (Recommended)

### Windows
```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Now install requirements
pip install -r requirements.txt
```

### macOS/Linux
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Now install requirements
pip install -r requirements.txt
```

## Common Setup Issues

### Issue: "pip not found"
```bash
# Use Python's pip module
python -m pip install -r requirements.txt
```

### Issue: Port 8000 already in use
```bash
# Use a different port
python manage.py runserver 8001
```

### Issue: Database errors
```bash
# Reset database (development only)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Issue: Template not found
```bash
# Verify app is in INSTALLED_APPS in settings.py
# Run: python manage.py migrate
```

## Verification Checklist

After setup, verify everything works:

- [ ] Server starts without errors
- [ ] Landing page loads at http://localhost:8000/
- [ ] Can navigate to registration page
- [ ] Can create a new account
- [ ] Can login with new account
- [ ] Can create a shortened URL
- [ ] Short URL redirects correctly
- [ ] QR code displays on detail page
- [ ] Admin panel accessible at /admin/
- [ ] Can view URLs in admin panel

## Project Structure Verification

Verify these files exist:
```
✓ manage.py
✓ requirements.txt
✓ db.sqlite3 (created after migrate)
✓ shortener/models.py
✓ shortener/views.py
✓ shortener/urls.py
✓ shortener/templates/shortener/*.html
✓ urlshortener/settings.py
✓ urlshortener/urls.py
```

## Running Tests

Verify the application code is working:
```bash
# Run all tests
python manage.py test shortener

# Run with verbose output
python manage.py test shortener -v 2

# Run specific test class
python manage.py test shortener.tests.ShortenedURLModelTest
```

Expected output: **15 tests, all OK** ✓

## Development Tips

### Enable Debug Toolbar (Optional)
```bash
pip install django-debug-toolbar
# Add to INSTALLED_APPS in settings.py
# Add middleware configuration
```

### Access Django Shell
```bash
python manage.py shell

# Example commands:
>>> from django.contrib.auth.models import User
>>> User.objects.all()
>>> from shortener.models import ShortenedURL
>>> ShortenedURL.objects.all()
```

### Create Sample Data
```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> from shortener.models import ShortenedURL
>>> user = User.objects.first()
>>> ShortenedURL.objects.create(
...     user=user,
...     original_url='https://example.com',
...     short_key='test123'
... )
```

## Stopping the Server

Press `Ctrl + C` in the terminal running the server.

On Windows if that doesn't work:
```bash
# Find the process
netstat -ano | findstr :8000

# Kill it (replace PID with the number shown)
taskkill /PID <PID> /F
```

## Resetting Everything

If something goes wrong and you want a fresh start:

```bash
# 1. Stop the server (Ctrl+C)

# 2. Delete database
rm db.sqlite3

# 3. Run migrations again
python manage.py migrate

# 4. Create new superuser
python manage.py createsuperuser

# 5. Start server
python manage.py runserver
```

## Next Steps

After successful setup:

1. **Read documentation**:
   - README.md - Full documentation
   - QUICKSTART.md - Quick reference
   - DEVELOPMENT.md - Development guide

2. **Customize** (optional):
   - Edit templates in `shortener/templates/`
   - Modify CSS in `shortener/static/css/`
   - Update colors in base.html

3. **Deploy** (when ready):
   - Follow DEVELOPMENT.md deployment checklist
   - Consider Heroku, AWS, or DigitalOcean

## Troubleshooting

### Check Python Version
```bash
python --version
# Expected: 3.8+
```

### Check Dependencies
```bash
pip list
# Should include: Django, qrcode, Pillow
```

### Check Database
```bash
python manage.py dbshell
# Shows SQLite prompt
# Type: .tables
# Exit: .quit
```

### Check URLs
```bash
python manage.py show_urls  # Django extension
# Or browse to /admin/ to verify routing
```

## Getting Help

1. **Review error messages** - They often tell you exactly what's wrong
2. **Check Django docs** - https://docs.djangoproject.com/
3. **Read the code** - Comments explain the logic
4. **Check logs** - Server console shows errors

## Production Considerations

Before deploying to production:

1. Set `DEBUG = False` in settings.py
2. Generate a new SECRET_KEY
3. Set `ALLOWED_HOSTS` to your domain
4. Use PostgreSQL instead of SQLite
5. Set up HTTPS/SSL
6. Configure static files serving
7. Set up environment variables
8. Configure logging

See DEVELOPMENT.md for details.

## Performance Tuning

### Database
```python
# Add indexes to frequently searched fields
# Use select_related() for foreign keys
# Use prefetch_related() for reverse relations
```

### Caching
```python
# Cache QR codes
# Cache click counts
# Use Redis for session storage
```

### Static Files
```bash
# Collect static files
python manage.py collectstatic --noinput

# Use CDN for serving
```

## Security Hardening

- [ ] Set `SECURE_SSL_REDIRECT = True`
- [ ] Set `SESSION_COOKIE_SECURE = True`
- [ ] Set `CSRF_COOKIE_SECURE = True`
- [ ] Set `SECURE_HSTS_SECONDS = 31536000`
- [ ] Use environment variables for secrets
- [ ] Implement rate limiting
- [ ] Add logging and monitoring
- [ ] Regular security updates

## Maintenance

### Regular Tasks
- Monitor server logs
- Check database size
- Review user activity
- Backup database regularly
- Update dependencies

### Backup Database
```bash
# SQLite backup
cp db.sqlite3 db.sqlite3.backup

# Or export for safekeeping
python manage.py dumpdata > backup.json
```

### Restore from Backup
```bash
python manage.py loaddata backup.json
```

---

You're all set! 🎉

Visit http://localhost:8000/ to start using the URL shortener.
