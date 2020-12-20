"""
Django development  settings for core project.
"""

import os
from .base import *

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = int(os.environ.get("DEBUG", default=1))

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")


MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
]

# Debug toolbar configuration


def show_toolbar(request):
    # callback to show debug toolbar independently from IPs because of docker
    if request.is_ajax():
        return False
    return True


CORS_ALLOW_ALL_ORIGINS = True


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}

INSTALLED_APPS += [
    "debug_toolbar",
]

# . as subdomain wildcard
# SESSION_COOKIE_DOMAIN = ".localhost"
SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_SECURE = False


SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", default=False)

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.environ.get("DB_NAME", "postgres"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST", "db"),
        "PORT": os.environ.get("DB_PORT", 5432),
    }
}

CONN_MAX_AGE = 180
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": os.path.join(BASE_DIR, "django_cache"),
        "TIMEOUT": 60,
    },
}

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "tmp", "mail")
