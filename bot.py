import os
import random
import telebot
from flask import Flask, request

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

MAULLIDOS = ["meow", "meow meow", "meeeoooow"]

# --- Lógica del Bot ---
@bot.message_handler(commands=['ask_figaro'])
def responder_comando(message):
    bot.reply_to(message, random.choice(MAULLIDOS))

@bot.message_handler(func=lambda message: message.chat.type == 'private')
def responder_privado(message):
    bot.reply_to(message, random.choice(MAULLIDOS))

@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route('/')
def home():
    return "Online", 200
