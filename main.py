import os
import telebot
from flask import Flask, request

API_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@bot.message_handler(func=lambda message: True)
def reply(message):
    bot.reply_to(message, "Спасибо! Я скоро отвечу.")

@app.route(f'/{API_TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

@app.route('/')
def index():
    bot.remove_webhook()
    bot.set_webhook(url=f"{os.environ.get('RENDER_URL')}/{API_TOKEN}")
    return 'Webhook установлен', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
