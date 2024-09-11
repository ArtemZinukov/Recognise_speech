import logging
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from df_google import detect_intent_texts
from environs import Env

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    df_response_text, df_response_status = detect_intent_texts(context.bot_data['project_id'],
                                                               context.bot_data['unique_session_id'],
                                                               user_message, 'ru')
    if df_response_text:
        update.message.reply_text(df_response_text)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Как я могу помочь?")


def main():
    env = Env()
    env.read_env()

    tg_bot = env.str("TG_BOT_TOKEN")
    project_id = env.str('PROJECT_ID')
    unique_session_id = env.str('TG_CHAT_ID')


    updater = Updater(tg_bot, use_context=True)
    while True:
        try:
            dispatcher = updater.dispatcher
            dispatcher.add_handler(CommandHandler("start", start))
            dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
            dispatcher.bot_data['project_id'] = project_id
            dispatcher.bot_data['unique_session_id'] = unique_session_id
            updater.start_polling()
            updater.idle()
        except Exception as e:
            logger.error(f"ТГ бот упал с ошибкой: {e}")

if __name__ == '__main__':
    main()