import os
import time
import csv
from flask import Flask, request
import telebot
from threading import Thread

API_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

TRIGGER_WORDS = ["код", "хочу", "сессия", "скидка", "интересно"]
USERS_DB = "clients.csv"

# Создание файла для базы клиентов
if not os.path.exists(USERS_DB):
    with open(USERS_DB, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["User ID", "Имя", "Username", "Сообщение", "Время"])

# Функция сохранения пользователя
def save_user_info(message):
    with open(USERS_DB, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            message.from_user.id,
            message.from_user.first_name,
            message.from_user.username,
            message.text,
            time.strftime('%Y-%m-%d %H:%M:%S')
        ])

# Стартовый автоответ
@bot.message_handler(func=lambda msg: any(word in msg.text.lower() for word in TRIGGER_WORDS))
def handle_trigger(msg):
    user_name = msg.from_user.first_name
    save_user_info(msg)

    # Блок 1: Приветствие
    bot.send_message(msg.chat.id, f"\U0001F31F Здравствуйте, {user_name}!
\nЭто Анастасия Гаврилова, автор метода 'Квантовый код изобилия'.\n\nБлагодарю за ваш интерес к трансформационной сессии! ✨\n\nУ меня для вас специальное предложение - скидка 20% действует ещё 3 дня.\n\nЧерез несколько секунд я отправлю вам важную информацию о сессии.\n\nА пока скажите, пожалуйста:\n- В какое время вам удобнее общаться?\n- Какой мессенджер предпочитаете для связи?")

    # Отложенное сообщение (через 10 секунд)
    def send_info_block():
        time.sleep(10)
        bot.send_message(msg.chat.id, "\U0001F4CB ТРАНСФОРМАЦИОННАЯ СЕССИЯ 'РАСКРЫТИЕ КОДА ИЗОБИЛИЯ'\n\n⏱ Длительность: 90 минут\n💰 Стоимость: 12,000₽ вместо 15,000₽ (скидка 20%)\n📅 Формат: индивидуально, онлайн\n\nЧто мы сделаем на сессии:\n✅ Расшифруем ваш уникальный нумерологический код\n✅ Выявим и трансформируем главный финансовый блок\n✅ Создадим персональный план активации изобилия\n✅ Проведём глубинную работу с подсознанием\n\nЧтобы я могла предложить вам максимально эффективную сессию, ответьте, пожалуйста, на 3 вопроса:\n1. Какая ваша главная финансовая задача сейчас?\n2. Какой результат хотите получить через месяц?\n3. Работали ли вы раньше с нумерологией или энергетическими практиками?")

    Thread(target=send_info_block).start()

# Вебхук
@app.route(f"/{API_TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "ok", 200

@app.route("/")
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"{os.environ.get('RENDER_URL')}/{API_TOKEN}")
    return "Webhook установлен", 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
