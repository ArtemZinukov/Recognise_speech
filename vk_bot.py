import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from df_google import detect_intent_texts
from environs import Env


def listen_for_messages(vk_session, project_id):
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            df_response_text, df_response_status = detect_intent_texts(project_id, event.user_id, event.text, 'ru')
            send_message_vk(df_response_text, vk_api, event)


def send_message_vk(df_response_text, vk_api, event):
    vk_api.messages.send(
        user_id=event.user_id,
        message=df_response_text,
        random_id=random.randint(1,1000)
    )


def main():
    env = Env()
    env.read_env()

    vk_bot_token = env.str("VK_BOT_TOKEN")
    project_id = env.str('PROJECT_ID')
    vk_session = vk_api.VkApi(token=vk_bot_token)
    listen_for_messages(vk_session, project_id)



if __name__ == '__main__':
    main()








