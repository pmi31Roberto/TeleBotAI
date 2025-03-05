from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters
import os
from mistralai import Mistral

# Токен Telegram-бота
TOKEN = '7646413054:AAGumbcZbvh8lG2-FxmVcz8pHLAxwsPPscQ'

# Инициализация клиента Mistral AI
mistral_client = Mistral(api_key='3QU1BC1nFuABWRF0ajJ2UaNTNrakj1Ys')


# Функция для обработки команды /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Привет! Я ваш бот с ИИ! Задайте мне вопрос.')


# Функция для обработки команды /help
async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text('Используйте /start, чтобы начать, или просто напишите мне сообщение.')


# Функция для обработки сообщений
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    try:
        # Новый вызов метода для взаимодействия с Mistral AI
        model = "codestral-latest"
        prompt = f"User: {user_message}\nAssistant:"
        response = mistral_client.fim.complete(
            model=model,
            prompt=prompt,
            temperature=0,
            top_p=1,
        )
        ai_response = response.choices[0].message.content
        await update.message.reply_text(ai_response)
    except Exception as e:
        await update.message.reply_text(f'Ошибка: {e}')


def main():
    # Создаем приложение и передаем токен
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    application.run_polling()


if __name__ == '__main__':
    main()
