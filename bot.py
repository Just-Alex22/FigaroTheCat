import os
import random
import telebot
from flask import Flask, request

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- Handler de Debug total ---
# Usamos un filtro más abierto y añadimos más info
@bot.message_handler(func=lambda message: True)
def responder_todo(message):
    print(f"DEBUG: ¡HANDLER DISPARADO! Texto: {message.text} | Chat ID: {message.chat.id}", flush=True)
    try:
        bot.reply_to(message, "Meow, te escucho!")
    except Exception as e:
        print(f"DEBUG: Error al intentar responder: {e}", flush=True)

@app.route('/webhook', methods=['POST'])
def get_message():
    print(f"DEBUG: ¡ENTRADA RECIBIDA! Headers: {request.headers}", flush=True)
    
    data = request.get_data().decode('utf-8')
    print(f"DEBUG: Contenido crudo: {data[:100]}", flush=True)
    
    if not data:
        return "OK", 200 

    try:
        update = telebot.types.Update.de_json(data)
        bot.process_new_updates([update])
        return "OK", 200
    except Exception as e:
        print(f"ERROR: {e}", flush=True)
        return "OK", 200 

@app.route('/')
def home():
    return "Fígaro está en línea", 200
