from django.db import models

class TelegramUser(models.Model):
    telegram_username = models.CharField(max_length=100)
