"""
Django settings for test project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    #    'django.contrib.admin',
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "crispy_forms",
    "captcha",
    "account",
    "main",
    "sponsor",
    "exhibitor",
    "devroom",
    "invoice",
    "parcel",
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

ROOT_URLCONF = "sabot.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.static",
                "sabot.template_processors.dates_processor",
                "sabot.template_processors.settings_processor",
                "sabot.template_processors.active_year_processor",
            ],
            "loaders": [
                ["django.template.loaders.app_directories.Loader"],
                ["django.template.loaders.filesystem.Loader"],
                ["sponsor.dbtemplateloader.DBLoader"],
            ],
        },
    }
]


WSGI_APPLICATION = "sabot.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/


USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

LOGIN_REDIRECT_URL = "/overview"

DATE_INPUT_FORMATS = ["%d.%m.%Y", "%d.%m.%y"]

CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

CRISPY_TEMPLATE_PACK = "bootstrap3"

REGISTRATION_OPEN = True
ACCOUNT_ACTIVATION_DAYS = 365

from sabot.local_settings import *
from sabot.conferenceSettings import *

if not DEBUG:
    template_loaders = TEMPLATES[0]["options"]["loaders"]
    TEMPLATES[0]["options"]["loaders"] = [
        ("django.template.loaders.cached.Loader", template_loaders)
    ]