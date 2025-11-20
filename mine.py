import os
from flask import Flask, request
import requests

TOKEN = os.getenv("BOT_TOKEN") or "YOUR_BOT_TOKEN"
URL = f"https://api.telegram.org/bot{TOKEN}/"

app = Flask(__name__)

# -----------------------------
# زخارف جاهزة
# -----------------------------
def decorate(text):
    styles = {
        "𝒁𝒂𝒌𝒉𝒓𝒂𝒇𝒂 1": text.replace("a", "𝒂").replace("b", "𝒃").replace("c", "𝒄"),
        "𝙕𝙖𝙠𝙝𝙧𝙖𝙛𝙖 2": text.replace("a", "𝗮").replace("b", "𝗯").replace("c", "𝗰"),
        "𝘼𝙍𝙏 𝙁𝙊𝙉𝙏": text.replace("a", "𝘼").replace("b", "𝘽").replace("c", "𝘾"),
        "𝘪𝘵𝘢𝘭𝘪𝘤𝘴": text.replace("a", "𝘢").replace("b", "𝘣").replace("c", "𝘤"),
        "҉ Ẓαкняɑƒ": f"҉ {text} ҉",
        "⸙ Decor": f"⸙ {text} ⸙"
    }
    return styles


# -----------------------------
# إرسال رسالة
# -----------------------------
def send_message(chat_id, text, reply=None):
    data = {
        "chat_id": chat_id,
        "text": text
    }
    if reply:
        data["reply_markup"] = reply
    requests.post(URL + "sendMessage", json=data)


# -----------------------------
# Webhook Receiver
# -----------------------------
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = request.json

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        if text == "/start":
            keyboard = {
                "keyboard": [[{"text": "✨ زخرف الآن"}]],
                "resize_keyboard": True
            }
            send_message(chat_id, "أهلاً بك 👋\nأرسل النص الذي تريد زخرفته.", keyboard)
            return "ok"

        elif text == "✨ زخرف الآن":
            send_message(chat_id, "أرسل النص الآن 🔤")
            return "ok"

        else:
            decorated = decorate(text)
            msg = "🔰 **نتيجة الزخرفة:**\n\n"
            for style in decorated.values():
                msg += f"{style}\n\n"
            send_message(chat_id, msg)
            return "ok"

    return "ok"


# -----------------------------
# Root
# -----------------------------
@app.route("/")
def home():
    return "Bot Running OK"


# -----------------------------
# تشغيل التطبيق
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
