# ================================
# manage.py
# ================================
#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'internship_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

# ================================
# requirements.txt
# ================================
"""
Django>=4.0
djangorestframework
python-decouple
djangorestframework-simplejwt
celery
redis
python-telegram-bot==13.15
"""

# ================================
# .env.example
# ================================
"""
SECRET_KEY=your_secret_key
TELEGRAM_TOKEN=your_telegram_bot_token
"""

# ================================
# internship_project/__init__.py
# ================================
from .celery import app as celery_app
__all__ = ['celery_app']

# ================================
# internship_project/settings.py
# ================================
from decouple import config
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config('SECRET_KEY')
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'core',
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

ROOT_URLCONF = 'internship_project.urls'
TEMPLATES = [{
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
}]
WSGI_APPLICATION = 'internship_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
CELERY_BROKER_URL = 'redis://localhost:6379/0'
TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')

# ================================
# internship_project/urls.py
# ================================
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# ================================
# internship_project/celery.py
# ================================
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'internship_project.settings')
app = Celery('internship_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# ================================
# core/apps.py
# ================================
from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

# ================================
# core/models.py
# ================================
from django.db import models

class TelegramUser(models.Model):
    telegram_username = models.CharField(max_length=100)

    def __str__(self):
        return self.telegram_username

# ================================
# core/admin.py
# ================================
from django.contrib import admin
from .models import TelegramUser

admin.site.register(TelegramUser)

# ================================
# core/views.py
# ================================
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class PublicAPI(APIView):
    def get(self, request):
        return Response({'message': 'This is a public API'})

class PrivateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': f'Hello, {request.user.username}!'})

# ================================
# core/urls.py
# ================================
from django.urls import path
from .views import PublicAPI, PrivateAPI

urlpatterns = [
    path('public/', PublicAPI.as_view()),
    path('private/', PrivateAPI.as_view()),
]

# ================================
# core/tasks.py
# ================================
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_welcome_email(user_email):
    send_mail(
        'Welcome!',
        'Thanks for registering.',
        'from@example.com',
        [user_email],
    )

# ================================
# core/management/commands/telegram_bot.py
# ================================
from django.core.management.base import BaseCommand
from telegram.ext import Updater, CommandHandler
from django.conf import settings
from core.models import TelegramUser

def start(update, context):
    username = update.message.from_user.username
    TelegramUser.objects.get_or_create(telegram_username=username)
    update.message.reply_text(f"Username saved: {username}")

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        updater = Updater(settings.TELEGRAM_TOKEN)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        updater.start_polling()
        updater.idle()
