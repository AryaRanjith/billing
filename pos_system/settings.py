import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env
load_dotenv(os.path.join(BASE_DIR, '.env'))

# SECURITY
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-temporary-key-change-later'
)

# DEBUG - Enable temporarily to see errors
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# HOSTS - Allow all in production (Render uses dynamic domains)
ALLOWED_HOSTS = ['*']

# CSRF - Dynamic CSRF origins for Render
CSRF_TRUSTED_ORIGINS = []
if os.environ.get('RENDER_EXTERNAL_URL'):
    CSRF_TRUSTED_ORIGINS.append(os.environ.get('RENDER_EXTERNAL_URL'))

# Required for Render HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'billing',
]

# MIDDLEWARE (correct order)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # must be high
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pos_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pos_system.wsgi.application'

import dj_database_url

# DATABASE (PostgreSQL for Render, SQLite for local fallback)
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# INTERNATIONAL
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# STATIC FILES (VERY IMPORTANT FOR RENDER)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Ensure staticfiles directory exists (but handle read-only filesystems like Vercel)
try:
    os.makedirs(STATIC_ROOT, exist_ok=True)
except OSError:
    # Read-only filesystem (e.g., Vercel), skip directory creation
    pass

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# DEFAULT PRIMARY KEY
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'