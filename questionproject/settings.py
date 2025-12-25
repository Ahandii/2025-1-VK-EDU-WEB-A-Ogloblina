from configparser import ConfigParser, ExtendedInterpolation
import os 

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.

ALLOWED_HOSTS = ['ogloblina.localhost', 'q.localhost', 'questions.localhost', '127.0.0.1', '0.0.0.0', 'localhost']

PROJECT_NAME = "questionproject"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read(os.path.join(BASE_DIR, PROJECT_NAME, 'prod.conf'))

DEBUG = False
SECRET_KEY = config.get("secret", "SECRET_KEY", fallback="!secret_key!")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_rename_app"
]

INSTALLED_APPS += [
    'questions',
    'core'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LOGIN_URL = "core:login"

ROOT_URLCONF = 'questionproject.urls'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "questions", 'templates'),
            os.path.join(BASE_DIR, "core", 'templates'),
            os.path.join(BASE_DIR, "questionproject", 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media'
            ],
            "builtins": [
                'questions.templatetags.index',
                'core.templatetags.form_extras'    
            ]
        },
    },
]

WSGI_APPLICATION = 'questionproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config.get('database', 'ENGINE', fallback='django.db.backends.postgresql'),
        'NAME': config.get('database', 'NAME'),
        'USER': config.get('database', 'USER'),
        'PASSWORD': config.get('database', 'PASSWORD'),
        'HOST': config.get('database', 'HOST', fallback='127.0.0.1'),
        'PORT': config.getint('database', 'PORT', fallback=5432),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "questionproject/static/"),
    os.path.join(BASE_DIR, "questions/static/"),
    os.path.join(BASE_DIR, "core/static"),
    #'static/',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')
