import os
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.InlineKeyboardMarkup()

    button = types.InlineKeyboardButton(
        "🖥️ Open Linux PC",
        callback_data="open_linux"
    )

    keyboard.add(button)

    bot.send_message(
        message.chat.id,
        "🖥️ Welcome to FreePC!\n\nনিচের button চাপুন Linux PC চালু করতে:",
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: call.data == "open_linux")
def open_linux(call):
    bot.answer_callback_query(call.id)

    bot.send_message(
        call.message.chat.id,
        "🚧 Linux Desktop এখনো সেটআপ করা হয়নি।\nStep 4-এ আমরা Free Linux Desktop তৈরি করব।"
    )

print("FreePC Bot is running...")
bot.infinity_polling()
