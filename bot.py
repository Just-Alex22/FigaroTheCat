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
    data = request.get_data().decode('utf-8')
    if not data:
        return "No data", 200
    
    print(f"DEBUG: Webhook recibió: {data[:150]}", flush=True)
    
    try:
        update = telebot.types.Update.de_json(data)
        
        # --- NUEVO: Inspección de objeto ---
        if update.message:
            print(f"DEBUG: Es un mensaje válido. ID: {update.message.message_id}", flush=True)
        else:
            print("DEBUG: El JSON recibido NO contiene un objeto 'message' válido.", flush=True)
            
        bot.process_new_updates([update])
        return "OK", 200
    except Exception as e:
        print(f"ERROR: {e}", flush=True)
        return "Error", 500

@app.route('/')
def home():
    return "Fígaro está en línea", 200
