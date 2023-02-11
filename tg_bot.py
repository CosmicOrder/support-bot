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
import uuid

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, \
    CallbackContext

from detect_intent_texts import detect_intent_texts
from logs_handlers import SupportLogsHandler


logger = logging.getLogger(__file__)


def provide_support(update: Update, context: CallbackContext) -> None:
    """Reply the user message."""

    project_id = os.getenv('PROJECT_ID')
    df_response = detect_intent_texts(project_id=project_id,
                                   session_id=uuid.uuid4(),
                                   language_code='eng',
                                   texts=update.message.text)

    update.message.reply_text(df_response.query_result.fulfillment_text)


def main() -> None:
    """Start the bot."""
    load_dotenv()
    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.DEBUG)

    support_bot_token = os.getenv('SUPPORT_BOT_TOKEN')
    chat_id = os.getenv('CHAT_ID')

    while True:
        try:
            updater = Updater(token=support_bot_token)
            logger.addHandler(SupportLogsHandler(updater.bot, chat_id))

            dispatcher = updater.dispatcher

            dispatcher.add_handler(
                MessageHandler(Filters.text & ~Filters.command, provide_support))

            updater.start_polling()
            logger.info("ТГ-бот запущен")

            updater.idle()
        except Exception as ex:
            logger.exception(ex)


if __name__ == '__main__':
    main()
