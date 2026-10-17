"""
Configuración de pruebas aisladas para BibliotecaVirtual.

No importa proyecto1.settings (evita ejecutar proyecto1/mongodb.py y, por lo tanto,
no abre conexión a MongoDB). Usa SQLite en memoria (:memory:) para que las pruebas
no escriban en db.sqlite3 ni modifiquen datos de desarrollo ni de MongoDB.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'test-insecure-key-do-not-use-in-production'
DEBUG = False
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'landing',
    'usuarios',
    'biblioteca',
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

ROOT_URLCONF = 'proyecto1.urls'

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

WSGI_APPLICATION = 'proyecto1.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Sin validadores para permitir contraseñas sencillas en pruebas.
AUTH_PASSWORD_VALIDATORS = []

# Hasher rápido para pruebas.
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Correo en memoria: no envía correos reales; se inspecciona con django.core.mail.outbox.
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
DEFAULT_FROM_EMAIL = 'tests@biblioteca.local'
