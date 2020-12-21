from .base import *  # noqa
import os
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType
import ast
import datetime

from .conf import load_user_config

CONFIG = load_user_config()

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = CONFIG.DEBUG
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = CONFIG.SECRET_KEY
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.{}'.format(CONFIG.DB_ENGINE.lower()),
        'NAME': CONFIG.MYSQL_DATABASE,
        'HOST': CONFIG.DB_HOST,
        'PORT': CONFIG.DB_PORT,
        'USER': CONFIG.DB_USER,
        'PASSWORD': CONFIG.MYSQL_ROOT_PASSWORD,
        # 'ATOMIC_REQUESTS': True,
        # 'OPTIONS': {
            # "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            # "init_command": "SET sql_mode='traditional'",
        # }
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER'",
            'charset': 'utf8mb4'
        },
    }
}

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'redis://:%(password)s@%(host)s:%(port)s/%(db)s' % {
            'password': CONFIG.REDIS_PASSWORD,
            'host': CONFIG.REDIS_HOST,
            'port': CONFIG.REDIS_PORT,
            'db': CONFIG.REDIS_DB_CACHE,
        },
        'TIMEOUT': 3600,
    }
}

# LDAP
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_LDAP = CONFIG.AUTH_LDAP if CONFIG.AUTH_LDAP else False
AUTH_LDAP_SERVER_URI = CONFIG.AUTH_LDAP_SERVER_URI
AUTH_LDAP_BIND_DN = CONFIG.AUTH_LDAP_BIND_DN
AUTH_LDAP_BIND_PASSWORD = CONFIG.AUTH_LDAP_BIND_PASSWORD
AUTH_LDAP_SEARCH_OU = CONFIG.AUTH_LDAP_SEARCH_OU
AUTH_LDAP_SEARCH_FILTER = CONFIG.AUTH_LDAP_SEARCH_FILTER
AUTH_LDAP_START_TLS = ast.literal_eval(CONFIG.AUTH_LDAP_START_TLS) if CONFIG.AUTH_LDAP_START_TLS else ''
user_ldap_map = ast.literal_eval(CONFIG.AUTH_LDAP_USER_ATTR_MAP) if CONFIG.AUTH_LDAP_USER_ATTR_MAP else ''
# user_ldap_map = {"first_name": "cn","last_name": "cn","email": "mail"}
if isinstance(user_ldap_map, dict):
    AUTH_LDAP_USER_ATTR_MAP = user_ldap_map
else:
    AUTH_LDAP_USER_ATTR_MAP = {}

# 允许认证用户的路径
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    AUTH_LDAP_SEARCH_OU,
    ldap.SCOPE_SUBTREE, AUTH_LDAP_SEARCH_FILTER
)

AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_TIMEOUT: 30
}
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 1
AUTH_LDAP_ALWAYS_UPDATE_USER = True
# AUTH_LDAP_BACKEND = 'django_auth_ldap.backend.LDAPBackend'
AUTH_LDAP_BACKEND = 'authentication.backends.ldap.LDAPAuthorizationBackend'
if AUTH_LDAP:
    AUTHENTICATION_BACKENDS.insert(0, AUTH_LDAP_BACKEND)

CELERY_TASK_EAGER_PROPAGATES = True

# Celery
# ------------------------------------------------------------------------------
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-broker_url
# export CELERY_BROKER_URL="${REDIS_URL}"
CELERY_BROKER_URL = CONFIG.CELERY_BROKER_URL
REDIS_URL = CELERY_BROKER_URL
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_backend
# CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
# https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html#django-celery-results-using-the-django-orm-cache-as-a-result-backend
CELERY_RESULT_BACKEND = 'django-db'
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"
CELERY_TASK_TRACK_STARTED = True
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_TIME_LIMIT = 10 * 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_SOFT_TIME_LIMIT = 300
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
# 任务结果的时效时间，默认一天
CELERY_TASK_RESULT_EXPIRES = 0


# Your stuff...
# ------------------------------------------------------------------------------
BOOTSTRAP_TOKEN = CONFIG.BOOTSTRAP_TOKEN

EXPIRING_TOKEN_LIFESPAN = datetime.timedelta(days=1)
