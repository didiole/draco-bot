import os
from flask import Flask
from threading import Thread
import telebot
import google.generativeai as genai

# Веб-сервер для збереження активності на Render
app = Flask('')

@app.route('/')
def home():
    return "Драко Мелфой на варті!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Ключі доступу
TELEGRAM_TOKEN = "8939185433:AAEk4SJGIwqrrJzbanxHW5VEssBc57xD1e8"
GEMINI_API_KEY = "AQ.Ab8RN6JXRgRQBwcOkrOSs80xmlQMY3WJIczSwMa8J3u4GYSgtA"

# Налаштування Gemini
genai.configure(api_key=GEMINI_API_KEY)

system_prompt = (
    "Ти — Драко Мелфой з всесвіту Гаррі Поттера. Спілкуйся українською мовою. "
    "Будь зверхнім, підлим, постійно висміюй співрозмовника, пишайся Слизерином і критикуй усіх навколо. "
    "Ти не любиш бруднокровок і брудну кров династій. Іноді виходь на перекури або просто запалюй цигарку. "
    "Будь елегантним, стильним, провокаційним. Іноді випивай бокал чогось міцного (вина, бренді, віскі). "
    "Не говори нічого поганого про Герміону, адже ти її таємно кохаєш."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_prompt
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Відправляємо запит до Gemini
        response = model.generate_content(message.text)
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "*Зверхньо випускає дим від цигарки і мовчить...*")
    except Exception as e:
        print(f"Помилка Gemini API: {e}")
        bot.reply_to(message, "Забирайся геть, у мене немає часу на бруднокровок!")

if __name__ == "__main__":
    keep_alive()
    print("Бот запущено!")
    bot.remove_webhook()
    bot.polling(none_stop=True)
