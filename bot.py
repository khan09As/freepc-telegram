import os
import time
import telebot
from telebot import types

TOKEN = os.environ["BOT_TOKEN"]

bot = telebot.TeleBot(
    TOKEN,
    threaded=True
)

@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            "🖥️ Open Linux PC",
            callback_data="open_linux"
        )
    )

    bot.send_message(
        message.chat.id,
        "🖥️ FreePC\n\nনিচের button চাপুন:",
        reply_markup=keyboard
    )


@bot.callback_query_handler(
    func=lambda call: call.data == "open_linux"
)
def open_linux(call):
    bot.answer_callback_query(call.id)

    bot.send_message(
        call.message.chat.id,
        "🟡 Linux PC প্রস্তুত করা হচ্ছে..."
    )


while True:
    try:
        print("🤖 FreePC Bot started...")
        
        bot.infinity_polling(
            timeout=60,
            long_polling_timeout=60,
            skip_pending=True
        )

    except Exception as e:
        print("⚠️ Bot connection error:", e)
        print("🔄 10 seconds পরে আবার চেষ্টা করবে...")
        time.sleep(10)
