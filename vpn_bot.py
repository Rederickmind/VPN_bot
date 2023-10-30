from outline_vpn.outline_vpn import OutlineVPN

import http
import logging
import os
import sys
import time
from http import HTTPStatus
from logging import StreamHandler

import requests
import telegram
from dotenv import load_dotenv
from telegram import Bot, ReplyKeyboardMarkup, TelegramError
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(message)s'
)
handler.setFormatter(formatter)

OUTLINE_API_URL = os.getenv('OUTLINE_API_URL')
CERT_SHA256 = os.getenv('CERT_SHA256')

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
# TELEGRAM_CHAT_ID =


updater = Updater(token=TELEGRAM_TOKEN)

# Setup the access with the API URL (Use the one provided to you after the server setup)
client = OutlineVPN(
    api_url=OUTLINE_API_URL,
    cert_sha256=CERT_SHA256
)

@Bot.message_handler(content_types=['text'])
def get_all_keys(OUTLINE_API_URL, CERT_SHA256,):
    """Get all access URLs on the server."""
    keys = [('ID ключа', 'Имя ключа', 'Ключ')]
    for key in client.get_keys():
        keys.append((key.key_id, key.name, key.access_url))
    for key in keys:
        print(key)

    button = ReplyKeyboardMarkup([['/get_keys']], resize_keyboard=True)
    chat_id = message.chat.id
    bot.send_message(chat_id, '\n'.join(map(str, a)))

def create_new_key():
    """Create new key."""
    key_dict = {}

    new_key = client.create_key(key_dict)


def rename_key(key_id, new_name):
    client.rename_key(key_id, new_name)

def rename_key(key_id):
    client.delete_key(key_id)


def add_data_limit(key_id, limit):
    """Set a monthly data limit int in MB"""
    client.add_data_limit(key_id, 1000 * 1000 * limit)


def remove_data_limit(key_id):
    """Remove the data limit."""
    client.delete_data_limit(key_id)


def check_tokens():
    """Проверка наличия токенов."""
    return all((TELEGRAM_TOKEN, OUTLINE_API_URL, CERT_SHA256))


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/start']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Это бот для управления ключами OUTLINE'.format(name),
        reply_markup=button
    )


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logger.critical('Отсутствуют необходимые токены.')
        raise sys.exit()

    updater = Updater(token=TELEGRAM_TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('get_keys', get_all_keys))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
