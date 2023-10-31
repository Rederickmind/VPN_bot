import logging
import os
import sys
from logging import StreamHandler

import requests
import telegram
from dotenv import load_dotenv
from telegram import Bot, ReplyKeyboardMarkup, TelegramError
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from outline_vpn.outline_methods import (add_data_limit, create_new_key,
                                         delete_key, get_all_keys,
                                         get_key_by_id, remove_data_limit)

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


updater = Updater(token=TELEGRAM_TOKEN)


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


def show_outline_keys(update, context):
    keys = get_all_keys(OUTLINE_API_URL, CERT_SHA256)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="\n\n".join(map(str, keys))
    )


def show_outline_key_by_id(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(
        chat_id=chat_id,
        text='What key do you want to select? Input key_id'
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text)
    )
    key_id = update.message.text
    key = get_key_by_id(key_id=key_id)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="\n".join(map(str, key))
    )


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logger.critical('Отсутствуют необходимые токены.')
        raise sys.exit()

    updater = Updater(token=TELEGRAM_TOKEN)

    updater.dispatcher.add_handler(
        CommandHandler(
            'start',
            wake_up
        )
    )
    updater.dispatcher.add_handler(
        CommandHandler(
            'get_keys',
            show_outline_keys
        )
    )
    updater.dispatcher.add_handler(
        CommandHandler(
            'get_key_by_id',
            show_outline_key_by_id
        )
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
