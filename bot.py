import os
import time
import requests
import telebot
from telebot import types

# ==================================================
# CONFIG
# ==================================================

BOT_TOKEN = os.environ["BOT_TOKEN"]
GH_TOKEN = os.environ["GH_TOKEN"]

# এখানে আপনার GitHub username বসান
REPO = "khan09As/freepc-telegram"

WORKFLOW = "linux-desktop.yml"

GITHUB_API = "https://api.github.com"

bot = telebot.TeleBot(
    BOT_TOKEN,
    threaded=True
)


# ==================================================
# GITHUB HEADERS
# ==================================================

def github_headers():
    return {
        "Authorization": f"Bearer {GH_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }


# ==================================================
# CHECK WHETHER LINUX WORKFLOW IS ALREADY RUNNING
# ==================================================

def linux_workflow_running():

    url = (
        f"{GITHUB_API}/repos/{REPO}/actions/workflows/"
        f"{WORKFLOW}/runs?per_page=10"
    )

    try:

        response = requests.get(
            url,
            headers=github_headers(),
            timeout=20
        )

        if response.status_code != 200:
            print(
                "GitHub status error:",
                response.status_code
            )

            # নিরাপত্তার জন্য API check ব্যর্থ হলে
            # নতুন workflow চালু করা হবে না
            return True

        runs = response.json().get(
            "workflow_runs",
            []
        )

        for run in runs:

            status = run.get("status")

            if status in [
                "queued",
                "in_progress",
                "waiting"
            ]:
                return True

        return False

    except Exception as e:

        print(
            "Workflow check error:",
            e
        )

        # নিরাপদ অবস্থান
        return True


# ==================================================
# MAIN MENU
# ==================================================

def send_main_menu(chat_id):

    keyboard = types.InlineKeyboardMarkup()

    keyboard.row(
        types.InlineKeyboardButton(
            "🖥️ Open Linux PC",
            callback_data="open_linux"
        )
    )

    keyboard.row(
        types.InlineKeyboardButton(
            "🗑️ Delete History",
            callback_data="delete_history"
        )
    )

    bot.send_message(
        chat_id,
        "🖥️ *FreePC*\n\n"
        "নিচের button নির্বাচন করুন:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )


# ==================================================
# START
# ==================================================

@bot.message_handler(commands=["start"])
def start(message):

    send_main_menu(
        message.chat.id
    )


# ==================================================
# OPEN LINUX PC
# ==================================================

@bot.callback_query_handler(
    func=lambda call: call.data == "open_linux"
)
def open_linux(call):

    chat_id = call.message.chat.id

    bot.answer_callback_query(
        call.id
    )

    # ------------------------------------------------
    # CHECK EXISTING WORKFLOW
    # ------------------------------------------------

    if linux_workflow_running():

        bot.send_message(
            chat_id,
            "⏳ *একটি Linux PC ইতিমধ্যে চালু আছে বা চালু হচ্ছে।*\n\n"
            "নতুন PC চালু করা যাবে না।\n"
            "বর্তমান PC বন্ধ হলে আবার চেষ্টা করুন।",
            parse_mode="Markdown"
        )

        return

    # ------------------------------------------------
    # START NEW GITHUB WORKFLOW
    # ------------------------------------------------

    bot.send_message(
        chat_id,
        "🟡 *Linux PC চালু করা হচ্ছে...*\n\n"
        "দয়া করে অপেক্ষা করুন।",
        parse_mode="Markdown"
    )

    url = (
        f"{GITHUB_API}/repos/{REPO}/actions/"
        f"workflows/{WORKFLOW}/dispatches"
    )

    headers = github_headers()

    # Workflow-এ Telegram chat ID পাঠানো হবে
    data = {
        "ref": "main",
        "inputs": {
            "chat_id": str(chat_id)
        }
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=30
        )

        if response.status_code == 204:

            bot.send_message(
                chat_id,
                "✅ *Linux PC চালু করার request পাঠানো হয়েছে!*\n\n"
                "Linux Desktop প্রস্তুত হলে "
                "আমি এখানে Desktop URL পাঠিয়ে দেব।",
                parse_mode="Markdown"
            )

        else:

            print(
                "GitHub workflow error:",
                response.status_code,
                response.text
            )

            bot.send_message(
                chat_id,
                "❌ Linux PC চালু করা যায়নি।\n\n"
                f"GitHub error: `{response.status_code}`",
                parse_mode="Markdown"
            )

    except Exception as e:

        print(
            "Workflow start error:",
            e
        )

        bot.send_message(
            chat_id,
            "❌ GitHub-এর সাথে যোগাযোগ করা যায়নি।\n"
            "কিছুক্ষণ পরে আবার চেষ্টা করুন।"
        )


# ==================================================
# DELETE HISTORY CONFIRMATION
# ==================================================

@bot.callback_query_handler(
    func=lambda call: call.data == "delete_history"
)
def delete_history(call):

    bot.answer_callback_query(
        call.id
    )

    keyboard = types.InlineKeyboardMarkup()

    keyboard.row(
        types.InlineKeyboardButton(
            "✅ Yes",
            callback_data="confirm_delete"
        ),
        types.InlineKeyboardButton(
            "❌ Cancel",
            callback_data="cancel_delete"
        )
    )

    bot.send_message(
        call.message.chat.id,
        "⚠️ *History মুছতে চান?*\n\n"
        "Telegram Bot API দিয়ে পুরো chat history "
        "একসাথে মুছে ফেলা যায় না।\n\n"
        "পুরো history মুছতে Telegram-এর "
        "Delete/Clear Chat ব্যবহার করুন।",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )


# ==================================================
# CONFIRM DELETE
# ==================================================

@bot.callback_query_handler(
    func=lambda call: call.data == "confirm_delete"
)
def confirm_delete(call):

    bot.answer_callback_query(
        call.id
    )

    bot.send_message(
        call.message.chat.id,
        "🗑️ History পরিষ্কার করতে Telegram-এর "
        "Chat Menu → Delete Chat/Clear History ব্যবহার করুন।"
    )


# ==================================================
# CANCEL DELETE
# ==================================================

@bot.callback_query_handler(
    func=lambda call: call.data == "cancel_delete"
)
def cancel_delete(call):

    bot.answer_callback_query(
        call.id,
        "Cancelled"
    )

    send_main_menu(
        call.message.chat.id
    )


# ==================================================
# INFINITY POLLING
# ==================================================

while True:

    try:

        print(
            "🤖 FreePC Bot started..."
        )

        bot.infinity_polling(
            timeout=60,
            long_polling_timeout=60,
            skip_pending=True
        )

    except Exception as e:

        print(
            "⚠️ Bot error:",
            e
        )

        time.sleep(10)
