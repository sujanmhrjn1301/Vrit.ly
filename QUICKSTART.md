# Quick Start Guide

## Getting Started in 5 Minutes

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Database Migrations
```bash
python manage.py migrate
```

### 3. Create Admin User (Optional)
```bash
python manage.py createsuperuser
```

### 4. Start the Development Server
```bash
python manage.py runserver
```

### 5. Access the Application
- **Main App**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/

## Using the Application

### First Time Users

1. **Visit the Landing Page**
   - Browse to http://localhost:8000/
   - Click "Create Account" button

2. **Create an Account**
   - Enter username, email, and password
   - Click "Create Account"
   - You'll be logged in automatically

3. **Create Your First Short URL**
   - Click "Create New URL" or "Create URL" in navigation
   - Paste your long URL
   - Optionally set an expiration date (in days)
   - Click "Create Short URL"

4. **Manage Your URLs**
   - View all URLs in Dashboard
   - Click "View" to see details and QR code
   - Click "Edit" to change the original URL
   - Click "Delete" to remove the URL
   - Customize the short code in the details page

### Features

#### Dashboard
- See all your shortened URLs
- View click counts
- See creation dates
- Check expiration status
- Quick actions (View, Edit, Delete)

#### URL Details
- View complete URL information
- Copy short URL to clipboard
- View/download QR code
- Check click analytics
- Customize short code
- Edit or delete URL

#### QR Codes
- Generated for **short URLs** only
- Can be downloaded as PNG files
- Perfect for sharing via print/posters
- Includes full short URL data

#### Analytics
- Track total clicks per URL
- View click timestamp and IP address
- Monitor user engagement
- Access click logs in admin panel

## Admin Features

### Access Admin Panel
1. Go to http://localhost:8000/admin/
2. Log in with superuser credentials
3. Manage users, URLs, and click logs

### Admin Tasks
- View all shortened URLs
- Monitor user accounts
- Check click statistics
- Search and filter URLs
- Export data if needed

## Common Tasks

### Change the Server Port
```bash
python manage.py runserver 8001
```

### Run with Specific Host
```bash
python manage.py runserver 0.0.0.0:8000
```

### Reset Database (Development Only)
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### View Database in Admin
1. Create superuser if not done
2. Go to `/admin/`
3. Login
4. Browse models

## Keyboard Shortcuts

- `/` - Focus on search (if implemented)
- `Ctrl+C` - Stop development server
- `Ctrl+D` - Logout (browser dependent)

## Troubleshooting

### Port 8000 Already in Use
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (Windows)
taskkill /PID <PID> /F

# Or use different port
python manage.py runserver 8001
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Database Errors
```bash
# Clear migrations and start fresh
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
```

### QR Code Not Showing
```bash
# Reinstall Pillow
pip install Pillow --upgrade
```

## Next Steps

- Deploy to production (Heroku, AWS, DigitalOcean)
- Add email notifications
- Implement REST API
- Add user profiles
- Create premium features
- Add social sharing
- Implement Google Analytics integration

## Project Structure Overview

```
shortener/              # Main app directory
├── models.py           # Database models
├── views.py            # View functions
├── forms.py            # Form definitions
├── urls.py             # URL routing
├── utils.py            # Helper functions
├── admin.py            # Admin configuration
├── templates/          # HTML templates
├── static/             # CSS, JS, images
└── migrations/         # Database migrations
```

## Important Files

- `manage.py` - Django management script
- `requirements.txt` - Python dependencies
- `db.sqlite3` - SQLite database (created after first run)
- `urlshortener/settings.py` - Django configuration
- `urlshortener/urls.py` - Main URL configuration

## Development Tips

1. **Hot Reload**: Changes to Python files automatically reload
2. **Debug Mode**: `DEBUG=True` shows detailed error pages
3. **Shell**: Run `python manage.py shell` for interactive Python
4. **Logging**: Check console for debug information
5. **Admin Interface**: Explore admin at `/admin/` for data inspection

## Getting Help

- Read `README.md` for detailed documentation
- Check Django documentation: https://docs.djangoproject.com/
- Review code comments in `views.py` and `models.py`
- Check browser console for frontend errors (F12)

---

**Happy URL shortening! 🚀**
