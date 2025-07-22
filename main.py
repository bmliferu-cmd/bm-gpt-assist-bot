import os
import openai
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters, ConversationHandler
)
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s — %(name)s — %(levelname)s — %(message)s',
    level=logging.INFO
)

# Состояния для ConversationHandler
AI_QUESTION = 1

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот активен. Ожидаю команды...")

# Обработка обычных сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"Принято: {text}")

# Команда /ai — вход в режим GPT
async def ai_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Напиши свой вопрос к ChatGPT:")
    return AI_QUESTION

# Обработка запроса к GPT
async def ai_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — ассистент, помогаешь сотрудникам выполнять задачи."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        reply = response['choices'][0]['message']['content']
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {str(e)}")
    return ConversationHandler.END

# Главная функция запуска
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Хендлеры
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Хендлер GPT с диалогом
    ai_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("ai", ai_command)],
        states={AI_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ai_process)]},
        fallbacks=[]
    )
    app.add_handler(ai_conv_handler)

    # Запуск
    app.run_polling()

if __name__ == '__main__':
    main()
