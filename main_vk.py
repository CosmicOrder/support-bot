import logging
import os
import random

import telegram
import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

from detect_intent_texts import detect_intent_texts
from logs_handlers import SupportLogsHandler

logger = logging.getLogger(__file__)


def support_reply(event, vk_api):
    df_reply = detect_intent_texts(project_id='ogeko-mfcu',
                                   session_id=12345,
                                   language_code='eng',
                                   texts=event.text)
    if df_reply:
        vk_api.messages.send(
            user_id=event.user_id,
            message=df_reply,
            random_id=random.randint(1, 1000)
        )


def main_vk(vk_group_token):
    vk_session = vk.VkApi(token=vk_group_token)
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)
    logger.info('VK-бот запущен')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            support_reply(event, vk_api)


if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.DEBUG)

    VK_GROUP_TOKEN = os.getenv('VK_GROUP_TOKEN')
    SUPPORT_BOT_TOKEN = os.getenv('SUPPORT_BOT_TOKEN')
    CHAT_ID = os.getenv('CHAT_ID')

    bot = telegram.Bot(token=SUPPORT_BOT_TOKEN)

    logger.addHandler(SupportLogsHandler(bot, CHAT_ID))

    while True:
        try:
            main_vk(VK_GROUP_TOKEN)
        except Exception as ex:
            logger.exception(ex)
