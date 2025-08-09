"""
Django settings for pythonnetworkmonitor project.
"""
from datetime import timedelta
from pathlib import Path
import os
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Use django-environ to read the .env file.
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DJANGO_DEBUG', default=False)

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "network_monitor",
    "rest_framework",
    "rest_framework_simplejwt",
    'django_celery_beat',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pythonnetworkmonitor.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "pythonnetworkmonitor.wsgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = 'America/Vancouver'

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
# STATIC_ROOT = BASE_DIR / "static_"
STATIC_ROOT = env('DJANGO_STATIC_ROOT', default=(BASE_DIR / 'staticfiles'))

STATICFILES_DIRS = [
    BASE_DIR / 'network_monitor' / 'static',
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- CELERY SETTINGS ---
CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/0')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/0')

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True

# --- CELERY BEAT SETTINGS ---
CELERY_BEAT_SCHEDULE = {
    # Task schedule to ping the hosts
    'ping_hosts_every_minute': {
        # The exact import path to your task.
        'task': 'network_monitor.tasks.schedule_tasks.ping_hosts',
        # The frequency for running the task.
        'schedule': timedelta(minutes=1),
    },
    # Task schedule to clean up the database.
    'delete_old_monitoring_data_daily': {
        'task': 'network_monitor.tasks.cleanup_tasks.delete_old_data',
        # Run once every 24 hours (daily)
        'schedule': timedelta(hours=24),
    },
}
