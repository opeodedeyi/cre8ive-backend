import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't_t)(gx@46mg-lyxnb+=t*pezz%+j+h1pz0=9(gzjhv3uv(lx7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'rest_auth',
    'rest_auth.registration',
    'accounts',
    'showcase',
    'collaborate',
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

ROOT_URLCONF = 'creativeAppApi.urls'

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

WSGI_APPLICATION = 'creativeAppApi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'email',
            'profile',
            'name'
        ],
        'AUTH_PARAMS': {
            'access_type': 'offline',
        },
        'APP': {
            # get from "console.developers.google.com/" then apis then credentials then oauthclient
            # fill in http://127.0.0.1:8000/accounts/google/login/callback/ in the “Authorized redirect URI” field
            'client_id': '63645136767-t0aqhv7ieuo7raf5lcsos2j5q3rsvr6c.apps.googleusercontent.com',
            'secret': 'jA5tysVYG6_3Tm5DsvWz8BgL',
            'key': ''
        }
    }
}


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
AUTH_USER_MODEL = 'accounts.User'
STATIC_URL = '/static/'

REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "accounts.api.serializers.CustomUserDetailsSerializer",
    'LOGIN_SERIALIZER': 'accounts.api.serializers.LoginSerializer',
    'PASSWORD_RESET_SERIALIZER': 'accounts.api.serializers.PasswordResetSerializer',
}

REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "accounts.api.serializers.CustomRegisterSerializer",
}

LOGIN_URL = "api/confirmed/"

ACCOUNT_ADAPTER = 'accounts.adapters.CustomUserAccountAdapter'
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = None #or "api/authenticated/"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_CONFIRMATION_HMAC = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
EMAIL_VERIFICATION = "mandatory"
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 3600
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 180
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"

SOCIALACCOUNT_EMAIL_REQUIRED = ACCOUNT_EMAIL_REQUIRED
SOCIALACCOUNT_STORE_TOKENS = True

# Email SMPT settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'opedoetester@gmail.com'
EMAIL_HOST_PASSWORD = '9ja4lifE'
DEFAULT_FROM_EMAIL = 'opedoetester@gmail.com'
DEFAULT_TO_EMAIL = EMAIL_HOST_USER
