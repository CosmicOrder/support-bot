import os
import random

import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

from detect_intent_texts import detect_intent_texts


def echo(event, vk_api):
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
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)


if __name__ == "__main__":
    load_dotenv()
    vk_group_token = os.getenv('VK_GROUP_TOKEN')

    main_vk(vk_group_token)
