import os
import random
import telebot
from flask import Flask, request

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

MAULLIDOS = ["meow", "meow meow", "meeeoooow"]

# --- Handlers con Debug ---
@bot.message_handler(commands=['ask_figaro'])
def responder_comando(message):
    print("DEBUG: Handler /ask_figaro detectado", flush=True)
    bot.reply_to(message, random.choice(MAULLIDOS))

@bot.message_handler(func=lambda message: True) # Catch-all para ver si cae cualquier cosa
def responder_todo(message):
    print(f"DEBUG: Handler universal detectado. Texto: {message.text}", flush=True)
    if message.chat.type == 'private':
        bot.reply_to(message, random.choice(MAULLIDOS))
    else:
        print("DEBUG: Mensaje no es privado, ignorando.", flush=True)

# --- Webhook ---
@app.route('/webhook', methods=['POST'])
def get_message():
    try:
        json_string = request.get_data().decode('utf-8')
        # Ya confirmamos que esto se imprime en tus logs
        print(f"DEBUG: Recibido en Webhook: {json_string[:100]}...", flush=True)
        
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "OK", 200
    except Exception as e:
        print(f"ERROR CRÍTICO: {e}", flush=True)
        return "Error interno", 500

@app.route('/')
def home():
    return "Fígaro está en línea", 200
