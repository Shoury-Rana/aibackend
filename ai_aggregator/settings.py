# ai_aggregator/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv # Import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file (for local development)
load_dotenv(os.path.join(BASE_DIR, '.env')) # Add this line

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Use environment variable for Secret Key
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-for-builds') # Provide a default for build phase

# SECURITY WARNING: don't run with debug turned on in production!
# Use environment variable for Debug, default to False for safety
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# --- Vercel Deployment Specific ---
# Vercel will automatically populate ALLOWED_HOSTS with the deployment URL
# For local dev, you might add 'localhost', '127.0.0.1' if needed via .env
# Or rely on DEBUG=True allowing them.
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
# Add Vercel's deployment URL pattern if DEBUG is False
if not DEBUG and os.environ.get('VERCEL_URL'):
    ALLOWED_HOSTS.append(f'.{os.environ.get("VERCEL_URL")}') # Allow *.your-project.vercel.app

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # Needed for Vercel builds even for API

    # Third-party apps
    'rest_framework',
    'corsheaders',

    # Your apps
    'endpoint',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Add WhiteNoise for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # CORS Middleware - place high up
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ai_aggregator.urls'

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

WSGI_APPLICATION = 'ai_aggregator.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# Using sqlite for simplicity, Vercel's free tier is ephemeral,
# so data won't persist between deployments anyway.
# For persistent data, you'd need an external DB (e.g., Neon, Supabase).
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
# Directory where `collectstatic` will gather static files for deployment
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Vercel needs this

# Enable WhiteNoise storage for static files (efficient serving)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- REST Framework Settings ---
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        # Add BrowsableAPIRenderer only if DEBUG is True for easier local testing
        ('rest_framework.renderers.BrowsableAPIRenderer' if DEBUG else None),
    ],
    # Add authentication/permission classes if needed later
    # 'DEFAULT_AUTHENTICATION_CLASSES': [],
    # 'DEFAULT_PERMISSION_CLASSES': [],
}

# --- CORS Settings ---
# Use environment variable for allowed origins
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
# Or, for more open development (less secure for production):
# CORS_ALLOW_ALL_ORIGINS = True # Use this carefully

# Allow credentials if your frontend needs to send cookies (e.g., for auth)
# CORS_ALLOW_CREDENTIALS = True

# --- AI API Keys (Loaded from .env) ---
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')