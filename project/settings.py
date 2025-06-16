import os
from pathlib import Path
from dotenv import load_dotenv
import firebase_admin

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")

CSRF_TRUSTED_ORIGINS = [
    "https://ride-production-f23c.up.railway.app",
    "http://ride-production-f23c.up.railway.app",
]

GDAL_LIBRARY_PATH = os.getenv('GDAL_LIBRARY_PATH', '/usr/lib/libgdal.so')

# Alternative common paths to try if the default doesn't work
possible_gdal_paths = [
    '/usr/lib/libgdal.so',
    '/usr/lib/x86_64-linux-gnu/libgdal.so',
    '/usr/local/lib/libgdal.so',
    '/lib/libgdal.so',
]

# Check which path exists
for path in possible_gdal_paths:
    if os.path.exists(path):
        GDAL_LIBRARY_PATH = path
        break

print(f"✅ GDAL_LIBRARY_PATH set to: {GDAL_LIBRARY_PATH}")

# Verify the file exists
if not os.path.exists(GDAL_LIBRARY_PATH):
    print(f"❌ Error: GDAL library not found at {GDAL_LIBRARY_PATH}")
    print("Please install GDAL and set the correct path:")
    print("On Ubuntu/Debian: sudo apt-get install gdal-bin libgdal-dev")
    print("Then locate the library with: find / -name 'libgdal.so*' 2>/dev/null")
else:
    print(f"✓ GDAL library found at {GDAL_LIBRARY_PATH}")
    
    
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "authentication",
    "location_field.apps.DefaultConfig",
    "rest_framework",
    "rest_framework.authtoken",
    "fcm_django",
    "django_filters",
    "channels",
    "core",
    "django.contrib.gis"
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

ROOT_URLCONF = "project.urls"

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

ASGI_APPLICATION = "project.asgi.application"
WSGI_APPLICATION = "project.wsgi.application"

if DEBUG:
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.contrib.gis.db.backends.postgis',
    #         'NAME': 'ride_db',
    #         'USER': 'postgres',
    #         'PASSWORD': 'cyparta@2024',
    #         'HOST': 'localhost',
    #         'PORT': '5432',
    #     }
    # }


    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.mysql',
    #         'NAME': 'scooter',
    #         'USER': 'root',
    #         'PASSWORD': 'cyparta@2024',
    #         'HOST':'localhost',
    #         'PORT':'3306',
    #     }
    # }
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite4",
            "NAME": os.path.join(BASE_DIR, "db.sqlite4"),
        }
    }

    # CHANNEL_LAYERS = {
    #     "default": {
    #         "BACKEND": "channels_redis.core.RedisChannelLayer",
    #         "CONFIG": {
    #             "hosts": [("127.0.0.1", 6379)],#192.168.1.8, 192.168.1.23
    #             # "prefix": "gradcam",
    #         },
    #     },
    # }

    # DATABASES = {
    #     "default": {
    #         "ENGINE": "django.db.backends.postgresql",
    #         "NAME": "railway",  # Replace with your actual DB name
    #         "USER": "postgres",  # Replace with your actual DB user
    #         "PASSWORD": "ujbmacKsYJwgzqDZyuCtXntbVfNBNxIE",  # Replace with your actual DB password
    #         "HOST": "postgres.railway.internal",  # Use Railway's host
    #         "PORT": "5432",  # PostgreSQL default port
    #     }
    # }
else:
    DATABASES = {
        "default": {
            "ENGINE": os.getenv("POSTGRES_ENGINE"),
            "NAME": os.getenv("POSTGRES_DB"),
            "USER": os.getenv("POSTGRES_USER"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "HOST": os.getenv("POSTGRES_HOSTNAME"),
            "PORT": os.getenv("POSTGRES_PORT"),
        }
    }

    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")
    REDIS_DB = os.getenv("REDIS_DB")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
    REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [REDIS_URL],
            },
        },
    }

    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    CELERY_REDBEAT_REDIS_URL = REDIS_URL
    CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
    CELERY_WORKER_SEND_TASK_EVENTS = True

AUTH_USER_MODEL = "authentication.User"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "EXCEPTION_HANDLER": "project.exception_handler.custom_exception_handler",
    "COERCE_DECIMAL_TO_STRING": False,
}

try:
    firebase_admin.get_app()
except ValueError:
    FCM_CREDENTIALS_PATH = os.path.join(
        BASE_DIR, "rides-7fe48-firebase-adminsdk-fbsvc-1f06aadce5.json"
    )
    cred = firebase_admin.credentials.Certificate(FCM_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)

FCM_DJANGO_SETTINGS = {
    "ONE_DEVICE_PER_USER": True,
    "DELETE_INACTIVE_DEVICES": True,
}
