import os
import random
import telebot
from flask import Flask, request

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.before_request
def log_every_request():
    print(f"DEBUG GLOBAL: Petición entrante: {request.method} {request.path} desde {request.remote_addr}", flush=True)
    if request.path == '/webhook':
        print(f"DEBUG GLOBAL: Headers: {dict(request.headers)}", flush=True)

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
    try:
        update = telebot.types.Update.de_json(data)
        
        # --- FORZAR RESPUESTA ---
        if update.message:
            chat_id = update.message.chat.id
            print(f"DEBUG: Intentando enviar mensaje a {chat_id}", flush=True)
            bot.send_message(chat_id, "¡Fígaro responde! (Prueba manual)")
            return "OK", 200
        
        return "OK (No es mensaje)", 200
    except Exception as e:
        print(f"ERROR: {e}", flush=True)
        return "Error", 500

@app.route('/')
@app.route('/')
def home():
    try:
        user = bot.get_me()
        return f"El bot {user.first_name} (@{user.username}) está conectado y listo.", 200
    except Exception as e:
        return f"Error con el token del bot: {str(e)}", 500
