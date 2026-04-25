import os
import random
import sys
import telebot
from flask import Flask, request

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    print("¡ERROR CRÍTICO: No se encontró el TOKEN en las variables de entorno!", flush=True)
else:
    print(f"Token detectado (longitud: {len(TOKEN)}). Inicializando bot...", flush=True)

bot = telebot.TeleBot(TOKEN) if TOKEN else None
app = Flask(__name__)

MAULLIDOS = ["meow", "meow meow", "meeeoooow"]

@bot.message_handler(commands=['ask_figaro'])
def responder_comando(message):
    bot.reply_to(message, random.choice(MAULLIDOS))

@bot.message_handler(func=lambda message: message.chat.type == 'private')
def responder_privado(message):
    bot.reply_to(message, random.choice(MAULLIDOS))

@app.route('/webhook', methods=['POST'])
def get_message():
    if not bot:
        return "Bot no configurado", 500
    try:
        json_string = request.get_data().decode('utf-8')
        print(f"DEBUG: Mensaje recibido: {json_string}", flush=True)
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "OK", 200
    except Exception as e:
        print(f"ERROR CRÍTICO: {e}", flush=True)
        return "Error interno", 500

@app.route('/')
def home():
    return "Fígaro está en línea", 200
