import logging
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from df_google import detect_intent_texts
from environs import Env
import time
from tg_logger import TelegramLogsHandler

logger = logging.getLogger(__name__)


def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    user_id =update.message.from_user.id
    df_response_text, df_response_status = detect_intent_texts(context.bot_data['project_id'],
                                                               user_id,
                                                               user_message, 'ru')
    if df_response_text:
        update.message.reply_text(df_response_text)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Как я могу помочь?")


def main():
    env = Env()
    env.read_env()

    tg_bot_token = env.str("TG_BOT_TOKEN")
    project_id = env.str('PROJECT_ID')
    unique_session_id = env.str('TG_CHAT_ID')
    tg_bot_logger_token = env.str("TG_BOT_LOGGER_TOKEN")

    tg_bot_logger = telegram.Bot(token=tg_bot_logger_token)

    updater = Updater(tg_bot_token, use_context=True)

    telegram_handler = TelegramLogsHandler(tg_bot_logger, unique_session_id)
    telegram_handler.setLevel(logging.INFO)
    telegram_formatter = logging.Formatter('%(message)s')
    telegram_handler.setFormatter(telegram_formatter)

    logger.addHandler(telegram_handler)
    logger.setLevel(logging.INFO)
    logger.info('Запуск бота')

    while True:
        try:
            dispatcher = updater.dispatcher
            dispatcher.add_handler(CommandHandler("start", start))
            dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
            dispatcher.bot_data['project_id'] = project_id
            updater.start_polling()
            updater.idle()
        except Exception:
            logger.exception("ТГ бот упал с ошибкой")
            time.sleep(5)

if __name__ == '__main__':
    main()