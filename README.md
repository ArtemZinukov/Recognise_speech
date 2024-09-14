# VK и Telegram Бот

Этот проект включает два бота: один для VK и один для Telegram. Боты используют Dialogflow для обработки пользовательских сообщений и логирования ошибок в Telegram.

## Описание

- **VK Бот**: Бот для VK, который обрабатывает сообщения пользователей и отвечает на них, используя Dialogflow.
- **TG Бот**: Бот для TG, который обрабатывает сообщения пользователей и отвечает на них, используя Dialogflow.
- **Telegram Логгер**: Бот для Telegram, который отправляет логи ошибок и информацию о работе VK бота в указанный чат.

## Установка

1. Клонируйте репозиторий:
   ```bash
   https://github.com/ArtemZinukov/Recognise_speech.git

2. Установите зависимости:

    ```bash
       pip install -r requirements.txt

## Настройка

Создайте файл .env в корневом каталоге проекта и добавьте следующие переменные окружения:

 - VK_BOT_TOKEN= ваш токен бота VK
 - PROJECT_ID= ваш ID проекта Dialogflow
 - TG_BOT_TOKEN= ваш токен бота Telegram
 - TG_CHAT_ID= ваш ID чата Telegram
 - TG_BOT_LOGGER_TOKEN= ваш токен логгера Telegram
 - GOOGLE_APPLICATION_CREDENTIALS= путь к файлу с ключами от Google

## Запуск

Для запуска бота выполните следующую команду:

```
python tg_bot.py
```

Или, если вы хотите запустить VK бота:

```
python vk_bot.py
```
