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


def provide_support(project_id, event, vk_api):
    session_id = f'vk-{event.user_id}'

    df_response = detect_intent_texts(project_id=project_id,
                                   session_id=session_id,
                                   language_code='eng',
                                   texts=event.text)

    if not df_response.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=df_response.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


def main():
    load_dotenv()
    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.DEBUG)

    project_id = os.getenv('PROJECT_ID')
    vk_group_token = os.getenv('VK_GROUP_TOKEN')
    support_bot_token = os.getenv('SUPPORT_BOT_TOKEN')
    chat_id = os.getenv('CHAT_ID')

    while True:
        try:
            bot = telegram.Bot(token=support_bot_token)

            logger.addHandler(SupportLogsHandler(bot, chat_id))

            vk_session = vk.VkApi(token=vk_group_token)
            vk_api = vk_session.get_api()

            longpoll = VkLongPoll(vk_session)
            logger.info('VK-бот запущен')
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    provide_support(project_id, event, vk_api)
        except Exception as ex:
            logger.exception(ex)


if __name__ == "__main__":
    main()
