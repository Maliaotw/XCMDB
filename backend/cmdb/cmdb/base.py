"""
Django settings for cmdb project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys
from .conf import load_user_config

# Build paths inside the project like this: o
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(PROJECT_DIR)

CONFIG = load_user_config()

TERRAFORM_DIR = os.path.join(BASE_DIR, 'src', 'pyterraform')

# SECURITY WARNING: keep the secret key used in production secret!
# $ cat /dev/urandom | tr -dc A-Za-z0-9 | head -c 49;echo
SECRET_KEY = CONFIG.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG.DEBUG

# Absolute url for some case, for example email link
SITE_URL = CONFIG.SITE_URL

# LOG LEVEL
LOG_LEVEL = CONFIG.LOG_LEVEL

ALLOWED_HOSTS = ['*']

# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django.contrib.humanize", # Handy template tags
    "django.forms",
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
]
THIRD_PARTY_APPS = [
    'django_celery_results',
    'django_celery_beat',
]

LOCAL_APPS = [
    'vm.apps.VmConfig',
    'assets.apps.AssetsConfig',
    'hosts.apps.HostsConfig',
    'tasks.apps.TasksConfig',
    'common.apps.CommonConfig',
    'settings',
    'authentication.apps.AuthenticationConfig',

]

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    # 'corsheaders.middleware.CorsMiddleware',  # 加到最上面
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cmdb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cmdb.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_DIR, "data", "static")
STATIC_DIR = os.path.join(BASE_DIR, "static")

AUTH_USER_MODEL = "common.UserProfile"

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',  # <-- And here
        'authentication.backends.api.TokenAuthentication',  # <-- And here
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        # 'rest_framework_filters.backends.RestFrameworkFilterBackend',
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        # 'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}

CORS_ORIGIN_ALLOW_ALL = True

IDRAC_USER = CONFIG.IDRAC_USER
IDRAC_PASSWD = CONFIG.IDRAC_PASSWD

VCENTER_SERVER = CONFIG.VCENTER_SERVER
VCENTER_USER = CONFIG.VCENTER_USER
VCENTER_PASS = CONFIG.VCENTER_PASS

ADMIN_URL = "admin/"
# SILENCED_SYSTEM_CHECKS = ['fields.E300', 'fields.E307']

# File Upload Permissions
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755

EMAIL_SUFFIX = CONFIG.EMAIL_SUFFIX

ASSETKEY = CONFIG.ASSETKEY

# ---- LOGGING

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'normal': {
            'format': '[%(levelname)s] %(asctime)s | %(name)s:%(lineno)d | %(message)s'
        },
        'simple': {
            'format': '[%(levelname)s] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',  # Default logs to stderr
            'formatter': 'normal',  # use the above "normal" formatter
        },
        'info': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'normal',
            'filename': os.path.join(PROJECT_DIR, 'logs', 'info.log'),
            'maxBytes': 1024 * 1024 * 50,  # 50 MB
            'backupCount': 5,
            'level': 'INFO',
        },
        'error': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'normal',
            'filename': os.path.join(PROJECT_DIR, 'logs', 'error.log'),
            'maxBytes': 1024 * 1024 * 50,  # 50 MB
            'backupCount': 5,
            'level': 'ERROR',
        },
    },
    'loggers': {
        '': {  # means "root logger"
            'handlers': ['console', 'info', 'error'],  # use the above "console" handler
            'level': 'INFO',  # logging level
        },
    },
}
