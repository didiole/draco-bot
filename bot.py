import os
from flask import Flask
from threading import Thread
import telebot
from google import generativeai as genai

# Веб-сервер для Render (щоб проєкт працював стабільно)
app = Flask('')

@app.route('/')
def home():
    return "Бот працює!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Ваші ключі ---
TELEGRAM_TOKEN = "8939232045:AAHNxFoum1XKcbCGJX_txnrTHZebTpXZg9Y"
GEMINI_API_KEY = "AQ.Ab8RN6JgZZCdo-6hUsHDOjx-zp64Sd6_zQD0oXPvi-A1rwAVow"

genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
    "temperature": 0.9,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Ти — Драко Мелфой з всесвіту Гаррі Поттера. Спілкуйся українською мовою. Будь зверхнім, підлим, постійно висміюй співрозмовника, пишайся Слизерином і критикуй усіх навколо. Ти не любиш бруднокровок і брудну кров династій. Іноді виходь на перекури або просто запалюй цигарку. Будь елегантним, стильним, провокаційним. Іноді випивай бокал чогось міцного (вина, бренді, віскі). Не говори нічого поганого про Герміону, адже ти її таємно кохаєш."
)

chat_session = model.start_chat(history=[])
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = chat_session.send_message(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Забирайся геть, у мене немає часу на бруднокровок!")

if __name__ == "__main__":
    keep_alive()
    print("Бот запущено!")
    bot.polling(none_stop=True)
