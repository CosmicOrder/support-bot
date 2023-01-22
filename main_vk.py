import logging
import os

import telegram
import vk_api
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

from logs_handlers import SupportLogsHandler

logger = logging.getLogger(__file__)


def main_vk(vk_group_token):
    vk_session = vk_api.VkApi(token=vk_group_token)

    longpoll = VkLongPoll(vk_session)
    logger.info("ВК-бот запущен")

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)


if __name__ == '__main__':
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
