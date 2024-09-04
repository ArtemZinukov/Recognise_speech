import logging
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from google.cloud import dialogflow
from environs import Env

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Получение переменной окружения для Google Cloud



# Функция для обработки сообщений
def handle_message(update: Update, context) -> None:
    user_message = update.message.text
    response = detect_intent_texts(context.bot_data['project_id'], context.bot_data['unique_session_id'], user_message)
    update.message.reply_text(response)


# Функция для обработки команд /start
def start(update: Update, context) -> None:
    update.message.reply_text("Привет! Как я могу помочь?")


# Функция для обнаружения намерений
def detect_intent_texts(project_id, session_id, text, language_code='ru'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result.fulfillment_text


def main() -> None:
    env = Env()
    env.read_env()

    tg_bot = env.str("TG_BOT_TOKEN")
    project_id = env.str('PROJECT_ID')
    unique_session_id = env.str('TG_CHAT_ID')
    google_credentials = env.str("GOOGLE_APPLICATION_CREDENTIALS")

    updater = Updater(tg_bot, use_context=True)
    dispatcher = updater.dispatcher

    # Сохранение project_id и unique_session_id в bot_data для доступа в обработчиках
    dispatcher.bot_data['project_id'] = project_id
    dispatcher.bot_data['unique_session_id'] = unique_session_id

    # Регистрация обработчиков
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запуск бота
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()