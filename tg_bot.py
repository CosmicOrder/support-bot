#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, \
    CallbackContext

from detect_intent_texts import detect_intent_texts
from logs_handlers import SupportLogsHandler


logger = logging.getLogger(__file__)


def support_reply(update: Update, context: CallbackContext) -> None:
    """Reply the user message."""

    df_reply = detect_intent_texts(project_id='ogeko-mfcu',
                                   session_id=12345,
                                   language_code='eng',
                                   texts=update.message.text)
    update.message.reply_text(df_reply)


def main() -> None:
    """Start the bot."""
    load_dotenv()
    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.DEBUG)

    SUPPORT_BOT_TOKEN = os.getenv('SUPPORT_BOT_TOKEN')
    CHAT_ID = os.getenv('CHAT_ID')

    updater = Updater(token=SUPPORT_BOT_TOKEN)
    logger.addHandler(SupportLogsHandler(updater.bot, CHAT_ID))

    dispatcher = updater.dispatcher

    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, support_reply))

    updater.start_polling()
    logger.info("ТГ-бот запущен")

    updater.idle()


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as ex:
            logger.exception(ex)
