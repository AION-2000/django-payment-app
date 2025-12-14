# 💳 Django Payment Gateway Application

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Django Version](https://img.shields.io/badge/django-4.0+-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A robust, enterprise-grade Django application featuring seamless payment processing, multi-provider authentication, and modern security implementations. Built with scalability and developer experience in mind.

---

## ✨ Core Capabilities

### 🔐 Authentication & Authorization
- **Multi-Provider Login System**
  - Traditional email/password authentication
  - Google OAuth 2.0 social authentication
  - Custom user model with email-based identification
  - Persistent session management with security hardening

### 💰 Payment Processing
- **Stripe Integration Suite**
  - PCI-compliant payment collection via Stripe Elements
  - Multi-wallet support (Google Pay, Apple Pay, Credit/Debit Cards)
  - Real-time payment confirmation
  - Automated webhook event processing
  - Comprehensive transaction logging and audit trails
  - Idempotent payment handling to prevent duplicates

### 🛡️ Security Infrastructure
- Google reCAPTCHA v2/v3 bot protection
- CSRF token validation on all state-changing requests
- Environment-based secrets management
- Production-ready security headers
- SQL injection prevention via ORM
- XSS protection mechanisms

### 🎨 User Interface
- Mobile-first responsive design with Bootstrap 5
- Accessible forms with real-time validation
- Intuitive error handling and user feedback
- Progressive enhancement for optimal performance

---

## 📁 Architecture Overview

```
django_payment_app/
│
├── 🔧 config/                      # Project configuration
│   ├── settings/
│   │   ├── base.py                 # Shared settings
│   │   ├── development.py          # Local development config
│   │   └── production.py           # Production optimizations
│   ├── urls.py                     # URL routing
│   └── wsgi.py / asgi.py           # WSGI/ASGI entry points
│
├── 🏠 core/                        # Core application logic
│   ├── views.py                    # Main view controllers
│   ├── models.py                   # Shared data models
│   └── templates/core/             # Base templates
│
├── 👤 accounts/                    # User management module
│   ├── models.py                   # Custom user model
│   ├── views.py                    # Auth views
│   ├── forms.py                    # Registration/login forms
│   └── templates/accounts/         # Auth UI templates
│
├── 💳 payments/                    # Payment processing module
│   ├── models.py                   # Transaction models
│   ├── views.py                    # Payment views
│   ├── webhooks.py                 # Stripe webhook handlers
│   └── templates/payments/         # Payment UI templates
│
├── 📦 static/                      # Static assets (CSS, JS, images)
├── 📄 requirements.txt             # Python dependencies
├── 🔒 .env.example                 # Environment template
└── 📖 README.md                    # This file
```

---

## 🚀 Getting Started

### System Requirements

| Component | Version |
|-----------|---------|
| Python | 3.8 or higher |
| Database | PostgreSQL 12+ (production) / SQLite (development) |
| Node.js | 14+ (for frontend tooling) |

### Initial Setup

**1. Clone and Navigate**
```bash
git clone https://github.com/yourusername/django-payment-app.git
cd django-payment-app
```

**2. Environment Setup**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

**3. Install Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**4. Environment Configuration**
```bash
# Create your environment file
cp .env.example .env

# Edit .env with your actual credentials
nano .env  # or use your preferred editor
```

**5. Database Initialization**
```bash
# Apply migrations
python manage.py migrate

# Create admin account
python manage.py createsuperuser

# (Optional) Load sample data
python manage.py loaddata fixtures/sample_data.json
```

**6. Launch Development Server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## ⚙️ Configuration Guide

### Environment Variables Reference

```bash
# ========================================
# Core Django Settings
# ========================================
SECRET_KEY=your-cryptographically-secure-secret-key
DEBUG=True  # Set to False in production
ENV=development  # Options: development, production
ALLOWED_HOSTS=localhost,127.0.0.1

# ========================================
# Database Configuration (PostgreSQL)
# ========================================
DB_NAME=payment_app_db
DB_USER=db_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432

# ========================================
# Google OAuth 2.0 Credentials
# ========================================
GOOGLE_OAUTH2_CLIENT_ID=xxxxx.apps.googleusercontent.com
GOOGLE_OAUTH2_CLIENT_SECRET=GOCSPX-xxxxx

# ========================================
# Stripe Payment Gateway
# ========================================
STRIPE_PUBLISHABLE_KEY=pk_test_xxxxx
STRIPE_SECRET_KEY=sk_test_xxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxx

# ========================================
# Google reCAPTCHA
# ========================================
RECAPTCHA_PUBLIC_KEY=6LeXXXXXXXXXXXXX
RECAPTCHA_PRIVATE_KEY=6LeXXXXXXXXXXXXX
```

### Development with HTTPS

Google Pay and Apple Pay require HTTPS even in development. Enable SSL locally:

```bash
# Install django-sslserver
pip install django-sslserver

# Run with SSL
python manage.py runsslserver 0.0.0.0:8000
```

---

## 🔌 Third-Party Service Configuration

### 🔑 Google OAuth Setup

1. Navigate to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable **Google+ API** from API Library
4. Configure OAuth consent screen with required scopes
5. Create OAuth 2.0 Client ID:
   - Application type: **Web application**
   - Authorized redirect URIs: `http://127.0.0.1:8000/accounts/google/login/callback/`
6. Copy credentials to `.env` file

### 💳 Stripe Configuration

1. Register at [Stripe Dashboard](https://dashboard.stripe.com/register)
2. Retrieve API keys from [API Keys page](https://dashboard.stripe.com/apikeys)
3. Configure webhook endpoint:
   - URL: `https://yourdomain.com/payments/webhook/`
   - Events to monitor:
     - `payment_intent.succeeded`
     - `payment_intent.payment_failed`
     - `charge.succeeded`
     - `charge.failed`
4. Add webhook signing secret to `.env`

**Local Webhook Testing:**
```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe  # macOS
# or download from https://stripe.com/docs/stripe-cli

# Forward events to local server
stripe listen --forward-to localhost:8000/payments/webhook/
```

### 🤖 reCAPTCHA Setup

1. Visit [reCAPTCHA Admin](https://www.google.com/recaptcha/admin/create)
2. Register your application:
   - Type: **reCAPTCHA v2** (Checkbox) or **v3**
   - Domains: `localhost`, `127.0.0.1` (dev) + production domain
3. Copy Site Key and Secret Key to `.env`

---

## 🧪 Testing

### Run Test Suite
```bash
# All tests
python manage.py test

# Specific app tests
python manage.py test accounts
python manage.py test payments

# With coverage report
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Payment Testing

**Test Card Numbers (Stripe):**
- Success: `4242 4242 4242 4242`
- Authentication Required: `4000 0025 0000 3155`
- Declined: `4000 0000 0000 9995`

Use any future expiry date and any 3-digit CVC.

---

## 🚢 Production Deployment

### Pre-Deployment Checklist

- [ ] Set `DEBUG=False` in production environment
- [ ] Configure production database (PostgreSQL recommended)
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Enable SSL/TLS certificates
- [ ] Configure static file serving (S3, CDN, etc.)
- [ ] Set up automated backups
- [ ] Configure error monitoring (Sentry, Rollbar)
- [ ] Review and apply security headers

### Deployment Commands

```bash
# Set production environment
export ENV=production

# Collect static files
python manage.py collectstatic --noinput

# Run with Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4

# Or with uWSGI
uwsgi --http :8000 --module config.wsgi --master --processes 4
```

### Recommended Production Stack

- **Web Server**: Nginx (reverse proxy + static files)
- **App Server**: Gunicorn or uWSGI
- **Database**: PostgreSQL with connection pooling
- **Cache**: Redis for sessions and caching
- **Task Queue**: Celery for background jobs
- **Monitoring**: Prometheus + Grafana or Datadog
- **SSL**: Let's Encrypt or commercial certificate

---

## 🔒 Security Considerations

### Implemented Protections

✅ Environment-based configuration management  
✅ CSRF protection on all forms  
✅ SQL injection prevention via Django ORM  
✅ XSS protection through template escaping  
✅ Secure password hashing (PBKDF2)  
✅ HTTPS enforcement in production  
✅ Content Security Policy headers  
✅ Rate limiting on authentication endpoints  

### Security Checklist

- Keep `SECRET_KEY` confidential and rotate periodically
- Use strong database passwords
- Enable 2FA on all external service accounts
- Regularly update dependencies: `pip list --outdated`
- Monitor application logs for suspicious activity
- Implement request rate limiting
- Use prepared statements for raw SQL queries
- Sanitize all user-generated content

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Standards

- Follow PEP 8 style guidelines
- Write tests for new features
- Update documentation as needed
- Use meaningful commit messages
- Keep PRs focused and concise

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support & Resources

- **Documentation**: [Full Documentation](https://docs.example.com)
- **Issues**: [GitHub Issues](https://github.com/yourusername/django-payment-app/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/django-payment-app/discussions)

### Helpful Links

- [Django Documentation](https://docs.djangoproject.com/)
- [Stripe API Reference](https://stripe.com/docs/api)
- [django-allauth Documentation](https://django-allauth.readthedocs.io/)

---

**Built with ❤️ Shihab Shahriar Aion**
