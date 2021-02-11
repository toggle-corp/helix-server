"""
Django settings for HELIX server project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import socket
import logging

from . import sentry

logger = logging.getLogger(__name__)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS_DIRNAME = 'apps'
APPS_DIR = os.path.join(BASE_DIR, APPS_DIRNAME)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY',
                            'w(m6)jr08z!anjsq6mjz%xo^*+sfnv$e3list=gfcfxaj_^4%o')
PRODUCTION = 'production'
DEVELOPMENT = 'development'
ALPHA = 'alpha'
NIGHTLY = 'nightly'
HELIX_ENVIRONMENT = os.environ.get('HELIX_ENVIRONMENT', DEVELOPMENT)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
logger.debug(f'\nServer running in {DEBUG=} mode.\n')

# FIXME:
ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOST', '*')]

# Application definition

LOCAL_APPS = [
    'contrib',
    'country',
    'users',
    'organization',
    'contact',
    'crisis',
    'event',
    'entry',
    'resource',
    'review',
    'extraction',
    'parking_lot',
    'contextualupdate',
    'report',
]

THIRD_PARTY_APPS = [
    'graphene_django',
    'rest_framework.authtoken',  # required by djoser
    'djoser',
    'corsheaders',
    'django_filters',
    'debug_toolbar',
    'graphene_graphiql_explorer',
    'graphiql_debug_toolbar',
    'django_dramatiq',
    'rest_framework',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
] + THIRD_PARTY_APPS + [
    # apps.users.apps.UsersConfig
    f'{APPS_DIRNAME}.{app}.apps.{"".join([word.title() for word in app.split("_")])}Config' for app in LOCAL_APPS
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'utils.middleware.DebugToolbarMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]
if HELIX_ENVIRONMENT not in (DEVELOPMENT,):
    MIDDLEWARE.append('django.middleware.clickjacking.XFrameOptionsMiddleware')

ROOT_URLCONF = 'helix.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'helix.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if os.environ.get('GITHUB_WORKFLOW'):
    print('Database github workflow')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            # in the workflow environment
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
            'PORT': 5432,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('POSTGRES_DB', 'postgres'),
            'USER': os.environ.get('POSTGRES_USER', 'postgres'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
            'HOST': os.environ.get('POSTGRES_HOST', 'db'),
            'PORT': os.environ.get('POSTGRES_PORT', 5432),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'users.User'

# https://docs.graphene-python.org/projects/django/en/latest/settings/
GRAPHENE = {
    'ATOMIC_MUTATIONS': True,
    'SCHEMA': 'helix.schema.schema',
    'SCHEMA_OUTPUT': 'schema.json',  # defaults to schema.json,
    'SCHEMA_INDENT': 2,  # Defaults to None (displays all data on a single line)
    'MIDDLEWARE': [
        'helix.sentry.SentryMiddleware',
    ],
}

GRAPHENE_DJANGO_EXTRAS = {
    'DEFAULT_PAGINATION_CLASS': 'graphene_django_extras.paginations.PageGraphqlPagination',
    'DEFAULT_PAGE_SIZE': 20,
    'MAX_PAGE_SIZE': 50,
    # 'CACHE_ACTIVE': True,
    # 'CACHE_TIMEOUT': 300    # seconds
}
if HELIX_ENVIRONMENT not in [DEVELOPMENT]:
    GRAPHENE['MIDDLEWARE'].append('utils.middleware.DisableIntrospectionSchemaMiddleware')

AUTHENTICATION_BACKEND = [
    'django.contrib.auth.backends.ModelBackend',
]

DJOSER = {
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': os.environ.get('SEND_ACTIVATION_EMAIL', "True") == 'True',
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'media/'

# https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-APPEND_SLASH
APPEND_SLASH = False

########
# CORS #
########

CORS_ORIGIN_WHITELIST = [
    "http://localhost:3080",
    "http://127.0.0.1:3080"
]
CORS_ALLOW_CREDENTIALS = True
# CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_REGEX_WHITELIST = [
#     '^https://[\w\-]+\.idmcdb\.org$'
# ]
# CSRF_TRUSTED_ORIGINS = []

#################
# DEBUG TOOLBAR #
#################

INTERNAL_IPS = [
    '127.0.0.1',
]

# https://github.com/flavors/django-graphiql-debug-toolbar/#installation
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS += [ip[:-1] + '1' for ip in ips]

# Django storage

# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
if HELIX_ENVIRONMENT not in (DEVELOPMENT,):
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'togglecorp-helix')
AWS_S3_REGION_NAME = os.environ.get('AWS_REGION', 'us-east-1')
AWS_QUERYSTRING_EXPIRE = int(os.environ.get('AWS_QUERYSTRING_EXPIRE', 12 * 60 * 60))
AWS_S3_FILE_OVERWRITE = False
AWS_IS_GZIPPED = True
GZIP_CONTENT_TYPES = [
    'text/css', 'text/javascript', 'application/javascript', 'application/x-javascript', 'image/svg+xml',
    'application/json',
]

SLS_SERVICE_NAME = os.environ.get('SLS_SERVICE_NAME', 'helix-serverless')
PDF_GENERATOR = os.environ.get('PDF_GENERATOR', 'generatePdf')
SLS_STAGES = {
    DEVELOPMENT: 'dev',
    PRODUCTION: 'prod',
    ALPHA: 'nightly',
    NIGHTLY: 'nightly'
}
sls_stage = SLS_STAGES[HELIX_ENVIRONMENT.lower()]
LAMBDA_HTML_TO_PDF = os.environ.get('LAMBDA_HTML_TO_PDF', f'{SLS_SERVICE_NAME}-{sls_stage}-{PDF_GENERATOR}')

# sign off admin emails
ENTRY_SIGNER_EMAILS = ','.split(os.environ.get('ENTRY_SIGNER_EMAILS', 'admin@helix.com'))

# Sentry Config
SENTRY_DSN = os.environ.get('SENTRY_DSN')

if SENTRY_DSN:
    SENTRY_CONFIG = {
        'dsn': SENTRY_DSN,
        'send_default_pii': True,
        # TODO: Move server to root directory to get access to .git
        # 'release': sentry.fetch_git_sha(os.path.dirname(BASE_DIR)),
        'environment': HELIX_ENVIRONMENT,
        'debug': DEBUG,
        'tags': {
            'site': ALLOWED_HOSTS[0],
        },
    }
    sentry.init_sentry(
        app_type='server',
        **SENTRY_CONFIG,
    )

RESOURCE_NUMBER = GRAPHENE_DJANGO_EXTRAS['MAX_PAGE_SIZE']
RESOURCEGROUP_NUMBER = GRAPHENE_DJANGO_EXTRAS['MAX_PAGE_SIZE']

# https://dramatiq.io/reference.html#middleware
DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.redis.RedisBroker",
    "OPTIONS": {"url": os.environ.get("DRAMATIQ_REDIS_URL", "redis://redis:6379/0")},
    "MIDDLEWARE": [
        "dramatiq.middleware.Prometheus",
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Callbacks",
        "dramatiq.middleware.Retries",
        "django_dramatiq.middleware.DbConnectionsMiddleware",
        "django_dramatiq.middleware.AdminMiddleware",
    ],
}

DRAMATIQ_TASKS_DATABASE = "default"

# FIXME: We can also configure result backend. what does that mean?kjj/dra
# TODO: Make tests work
