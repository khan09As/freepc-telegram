import os
import telebot
from telebot import types

TOKEN = os.environ["BOT_TOKEN"]
bot = telebot.TeleBot(TOKEN)

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

@bot.callback_query_handler(func=lambda call: call.data == "open_linux")
def open_linux(call):
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "🟡 Linux PC প্রস্তুত করা হচ্ছে..."
    )

bot.infinity_polling()
