import os
import openai
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from datetime import datetime, timedelta

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот активен. Ожидаю задачи 🧠")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"Принято: {text} (в будущем я это распарсю)")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
@bot.message_handler(commands=['ai'])
def handle_ai(message):
    msg = bot.send_message(message.chat.id, "Напиши свой вопрос к ChatGPT:")
    bot.register_next_step_handler(msg, process_ai_prompt)

def process_ai_prompt(message):
    prompt = message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — ассистент, помогаешь сотрудникам выполнять задачи."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        reply = response['choices'][0]['message']['content']
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
