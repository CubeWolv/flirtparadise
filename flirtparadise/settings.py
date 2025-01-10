"""
Django settings for flirtparadise project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pqv%pn&&47i71hx#vkt7(d!0d$asx^*-z!_u3w$sg&)!s9@c58'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'flirtparadise-production.up.railway.app',
    '127.0.0.1',
    'localhost',
    'flirtparadise.xyz'
]


CSRF_TRUSTED_ORIGINS = [
    'https://flirtparadise.xyz'
]


SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = False

SITE_URL = "https://flirtparadise.xyz"
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'gender',
    'rest_framework',
    "whitenoise.runserver_nostatic",
    'django.contrib.sitemaps',
    'flirtparadise'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.gzip.GZipMiddleware',
]

ROOT_URLCONF = 'flirtparadise.urls'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #'blog.context_processors.seo_processor',
            ],
        },
    },
]
WSGI_APPLICATION = 'flirtparadise.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set")

DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL)
}

# Ensure ENGINE is set properly
DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
MEDIA_URL = '/media/'  # URL to serve media files
MEDIA_ROOT = os.path.join('/mnt/volumes', 'media') 

STATIC_URL = '/static/'
STATICFILES = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, './static/')]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# settings.py
FLUTTERWAVE_PUBLIC_KEY = 'FLWPUBK_TEST-7498309ef5111c01eb2a708032accc0b-X'
FLUTTERWAVE_SECRET_KEY = 'FLWSECK_TEST-1516083e6f90b0d3232180837c29902f-X'


LOGIN_URL = 'login'



GZIP_CONTENT_TYPES = [
    'text/plain',
    'text/html',
    'text/css',
    'application/javascript',
    'application/json',
    'application/xml',
    'font/woff2',
    # Add any other mime types you want to compress
]

# Optionally, set the minimum size of the response to be compressed (in bytes)
GZIP_MIN_LENGTH = 1000
