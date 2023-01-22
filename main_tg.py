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
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, \
    CallbackContext

# Enable logging
from detect_intent_texts import detect_intent_texts
from logs_handlers import SupportLogsHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__file__)


# Define a few command handlers. These usually take the two arguments update
# and context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Здравствуйте')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    df_reply = detect_intent_texts(project_id='ogeko-mfcu',
                                   session_id=12345,
                                   language_code='eng',
                                   texts=update.message.text)
    update.message.reply_text(df_reply)


def main(support_bot_token) -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=support_bot_token)
    logger.addHandler(SupportLogsHandler(updater.bot, CHAT_ID))

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()
    logger.info("ТГ-бот запущен")

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.DEBUG)

    SUPPORT_BOT_TOKEN = os.getenv('SUPPORT_BOT_TOKEN')
    CHAT_ID = os.getenv('CHAT_ID')

    while True:
        try:
            main(SUPPORT_BOT_TOKEN)
        except Exception as ex:
            logger.exception(ex)
