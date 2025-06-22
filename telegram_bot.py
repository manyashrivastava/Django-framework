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
