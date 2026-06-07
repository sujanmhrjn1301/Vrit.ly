# URL Shortener Web Application

A modern Django-based URL shortener application similar to TinyURL or Bitly. Create short, memorable links and track their analytics with built-in QR code generation.

## Features

### Core Features
- **URL Shortening**: Convert long URLs into short, shareable links using base62 encoding
- **User Authentication**: Register, login, and logout functionality
- **URL Management**: Create, view, edit, and delete shortened URLs
- **Custom Short Codes**: Personalize your short URLs with custom codes
- **Analytics**: Track click counts and access statistics
- **QR Code Generation**: Generate QR codes for easy sharing (for short URLs, not original URLs)
- **URL Expiration**: Set expiration dates for temporary shortened URLs
- **Click Logging**: Record detailed information about clicks (IP address, user agent, timestamp)

### Technical Highlights
- Base62 encoding for short URL generation
- Click tracking with IP and user agent logging
- Responsive Bootstrap 5 UI
- Django admin panel for management
- SQLite database (easily switchable to PostgreSQL/MySQL)

## Installation

### Prerequisites
- Python 3.8+
- Django 4.2
- qrcode 8.2
- Pillow 10.0.0

### Setup

1. **Clone/Navigate to the project directory**
   ```bash
   cd "d:\Python 2.0\Vrit.ly (v.2.0)"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser for admin access**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Main app: http://localhost:8000/
   - Admin panel: http://localhost:8000/admin/

## Project Structure

```
urlshortener/
├── urlshortener/          # Project settings
│   ├── settings.py        # Django configuration
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # WSGI configuration
├── shortener/             # Main app
│   ├── migrations/        # Database migrations
│   ├── templates/         # HTML templates
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
│   ├── static/            # Static files (CSS, JS)
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── forms.py           # Django forms
│   ├── urls.py            # App URL routing
│   ├── utils.py           # Helper functions
│   └── admin.py           # Admin configuration
├── manage.py              # Django management script
├── db.sqlite3             # Database file
└── requirements.txt       # Dependencies

```

## Database Models

### ShortenedURL
- **user**: ForeignKey to User (cascade delete)
- **original_url**: URLField for the long URL
- **short_key**: Unique auto-generated base62 code
- **custom_key**: Optional custom short code
- **click_count**: Counter for redirect clicks
- **created_at**: Timestamp of creation
- **updated_at**: Last modification timestamp
- **expires_at**: Optional expiration datetime
- **is_active**: Boolean flag for soft deletion

### URLClickLog
- **shortened_url**: ForeignKey to ShortenedURL
- **clicked_at**: Click timestamp
- **ip_address**: Client IP address
- **user_agent**: Browser/client information

## URLs and Routes

### Public Routes
| Route | Purpose |
|-------|---------|
| `/` | Landing page |
| `/register/` | User registration |
| `/login/` | User login |
| `/logout/` | User logout |
| `/s/<short_code>/` | Redirect to original URL |

### Authenticated Routes
| Route | Purpose |
|-------|---------|
| `/dashboard/` | View all shortened URLs |
| `/create/` | Create new shortened URL |
| `/url/<id>/` | View URL details and analytics |
| `/url/<id>/edit/` | Edit URL |
| `/url/<id>/delete/` | Delete URL |
| `/url/<id>/qr/` | Get QR code as JSON |

## Features in Detail

### 1. User Registration & Authentication
- Create account with username, email, and password
- Password validation and confirmation
- Secure login/logout functionality
- Session-based authentication

### 2. URL Shortening Algorithm
Uses Base62 encoding to generate unique, short codes:
- Supports 62 characters (0-9, a-z, A-Z)
- 6-character codes provide ~56 billion combinations
- Auto-regenerates if collision detected
- Optional custom codes with uniqueness validation

### 3. Analytics & Tracking
- Click counter for each URL
- IP address tracking
- User agent logging
- Click timestamp recording
- Dashboard statistics display

### 4. QR Code Generation
- Generates QR codes for shortened URLs (not original URLs)
- Base64 encoded for inline display
- Downloadable as PNG files
- Supports all QR code standards

### 5. URL Management
- Create URLs with optional expiration dates
- Edit original URL after creation
- Customize short codes
- Soft delete with is_active flag
- Expiration date enforcement

## Admin Panel Features

Access Django admin at `/admin/`:
- Manage all URLs and users
- View click logs
- Filter by user, date, and activity
- Search by URL or short code
- Monitor system usage

## Security Features

- CSRF protection enabled
- Password hashing with Django authentication
- SQL injection prevention via ORM
- User-specific URL access control
- Soft deletes for data preservation

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

## Production Deployment

For production deployment:

1. **Update settings.py**
   - Set `DEBUG = False`
   - Add domain to `ALLOWED_HOSTS`
   - Use environment variables for `SECRET_KEY`
   - Configure proper database (PostgreSQL recommended)

2. **Security**
   - Use HTTPS only
   - Set `SECURE_SSL_REDIRECT = True`
   - Configure CORS if needed
   - Use environment variables for sensitive data

3. **Database**
   - Switch to PostgreSQL or MySQL
   - Set up backups
   - Enable connection pooling

4. **Deployment**
   - Use Gunicorn/uWSGI as WSGI server
   - Configure Nginx as reverse proxy
   - Set up caching (Redis)
   - Enable logging and monitoring

## API Endpoints (Future)

The application can be extended with REST API endpoints:
- `GET /api/urls/` - List user's URLs
- `POST /api/urls/` - Create new URL
- `GET /api/urls/{id}/` - Get URL details
- `PUT /api/urls/{id}/` - Update URL
- `DELETE /api/urls/{id}/` - Delete URL
- `GET /api/urls/{id}/stats/` - Get click statistics

## Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Database Locked
Delete `db.sqlite3` and run migrations again:
```bash
rm db.sqlite3
python manage.py migrate
```

### QR Code Not Displaying
Ensure Pillow is installed:
```bash
pip install Pillow --upgrade
```

## License

MIT License - Feel free to use this project for personal or commercial purposes.

## Support

For issues or questions, check the Django documentation or raise an issue in the repository.

---

**Built with Django 4.2** | **Bootstrap 5** | **SQLite/PostgreSQL**
