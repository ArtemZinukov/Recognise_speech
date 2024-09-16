import random
import logging
import traceback

import telegram
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from df_google import detect_intent_texts
from environs import Env
import time
from tg_logger import TelegramLogsHandler

logger = logging.getLogger(__name__)


def listen_for_messages(vk_session, project_id):
    vk_api_instance = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            df_response_text, df_response_status = detect_intent_texts(project_id, event.user_id, event.text, 'ru')
            if not df_response_status:
                send_message_vk(df_response_text, vk_api_instance, event)



def send_message_vk(message_text, vk_api_instance, event):
    vk_api_instance.messages.send(
        user_id=event.user_id,
        message=message_text,
        random_id=random.randint(1, 1000)
    )


def main():
    env = Env()
    env.read_env()

    vk_bot_token = env.str("VK_BOT_TOKEN")
    project_id = env.str('PROJECT_ID')
    tg_bot_logger_token = env.str("TG_BOT_LOGGER_TOKEN")
    tg_chat_id = env.str("TG_CHAT_ID")

    tg_bot = telegram.Bot(token=tg_bot_logger_token)

    telegram_handler = TelegramLogsHandler(tg_bot, tg_chat_id)
    telegram_handler.setLevel(logging.INFO)
    telegram_formatter = logging.Formatter('%(message)s')
    telegram_handler.setFormatter(telegram_formatter)

    logger.addHandler(telegram_handler)
    logger.setLevel(logging.INFO)
    logger.info('Запуск бота')

    while True:
        try:
            vk_session = vk_api.VkApi(token=vk_bot_token)
            listen_for_messages(vk_session, project_id)
        except vk_api.ApiError as err:
            logger.error(f"Ошибка VK API: {err}")
            time.sleep(5)
        except Exception:
            logger.exception("Произошла ошибка")
            time.sleep(5)


if __name__ == '__main__':
    main()