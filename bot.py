import os
import random
import telebot
from flask import Flask, request

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
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
    try:
        json_string = request.get_data().decode('utf-8')
        print(f"DEBUG: Datos recibidos: {json_string}")
        
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "OK", 200
    except Exception as e:
        print(f"ERROR CRÍTICO EN WEBHOOK: {e}")
        return "Error interno", 500

@app.route('/')
def home():
    return "Fígaro está en línea", 200
