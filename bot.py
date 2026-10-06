import os
import time
import requests
import telebot
from telebot import types

TOKEN = os.environ["BOT_TOKEN"]
GH_TOKEN = os.environ["GH_TOKEN"]

REPO = "khan09As/freepc-telegram"
WORKFLOW = "linux-desktop.yml"

bot = telebot.TeleBot(TOKEN, threaded=True)


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
        "🟡 Linux PC চালু করা হচ্ছে..."
    )

    url = f"https://api.github.com/repos/{REPO}/actions/workflows/{WORKFLOW}/dispatches"

    headers = {
        "Authorization": f"Bearer {GH_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    data = {
        "ref": "main"
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=30
    )

    if response.status_code == 204:
        bot.send_message(
            call.message.chat.id,
            "✅ Linux PC চালু করার request পাঠানো হয়েছে!\n\n"
            "কিছুক্ষণ পর Desktop URL পাওয়া যাবে।"
        )
    else:
        bot.send_message(
            call.message.chat.id,
            f"❌ Linux PC চালু করা যায়নি.\n"
            f"GitHub error: {response.status_code}"
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
        print("⚠️ Error:", e)
        time.sleep(10)
