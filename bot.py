import os
import telebot

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def responder(message):
    print(f"DEBUG: Mensaje recibido: {message.text}", flush=True)
    bot.reply_to(message, "¡Meow! Estoy vivo (vía polling).")

print("DEBUG: Iniciando polling...", flush=True)
bot.infinity_polling()
