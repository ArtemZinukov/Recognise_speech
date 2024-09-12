import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env


def listen_for_messages(vk_session):
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            handle_new_message(event)


def handle_new_message(event):
    print('Новое сообщение:')
    if event.to_me:
        print('Для меня от: ', event.user_id)
    else:
        print('От меня для: ', event.user_id)
    print('Текст:', event.text)


def main():
    env = Env()
    env.read_env()

    vk_bot_token = env.str("VK_BOT_TOKEN")
    vk_session = vk_api.VkApi(token=vk_bot_token)
    listen_for_messages(vk_session)


if __name__ == '__main__':
    main()