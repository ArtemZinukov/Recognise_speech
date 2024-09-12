import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env


def listen_for_messages(vk_session):
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1,1000)
    )


def main():
    env = Env()
    env.read_env()

    vk_bot_token = env.str("VK_BOT_TOKEN")
    vk_session = vk_api.VkApi(token=vk_bot_token)
    listen_for_messages(vk_session)



if __name__ == '__main__':
    main()








