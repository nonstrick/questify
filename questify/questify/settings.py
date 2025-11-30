from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')

SECRET_KEY = 'django-insecure-zbigu6d4wz82&m8lbp8oi)a2n#tu7vbz_unxt^kt8=+a3qu5rt'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'home',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'questify.urls'

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

WSGI_APPLICATION = 'questify.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'home.validators.RussianUserAttributeSimilarityValidator',
        'OPTIONS': {
            'user_attributes': ('username', 'email'),
        }
    },
    {
        'NAME': 'home.validators.RussianMinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'home.validators.RussianCommonPasswordValidator',
    },
    {
        'NAME': 'home.validators.RussianNumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/profile/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

GIGACHAT_CREDENTIALS = os.environ.get('GIGACHAT_CREDENTIALS', '')
GIGACHAT_AUTH_KEY = os.environ.get('GIGACHAT_AUTH_KEY', '')
GIGACHAT_CLIENT_ID = os.environ.get('GIGACHAT_CLIENT_ID', '')
GIGACHAT_CLIENT_SECRET = os.environ.get('GIGACHAT_CLIENT_SECRET', '')
GIGACHAT_SCOPE = os.environ.get('GIGACHAT_SCOPE', 'GIGACHAT_API_PERS')
GIGACHAT_VERIFY_SSL = os.environ.get('GIGACHAT_VERIFY_SSL', 'False')
GIGACHAT_CERT_PATH = os.environ.get('GIGACHAT_CERT_PATH', '')
