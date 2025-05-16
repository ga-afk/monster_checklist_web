import os
print("Current working dir:", os.getcwd())
from flask import Flask, request, render_template, redirect, url_for
import json
import os
import requests

app = Flask(__name__)
CHECKLIST_FILE = "checklist.json"

TELEGRAM_TOKEN = "7794577995:AAETws32jHm5W_UuSUJN-D29aiTL5XAnxKs"
TELEGRAM_CHAT_ID = None  # Автоматично оновиться після першого повідомлення

def send_telegram_message(text):
    global TELEGRAM_CHAT_ID
    if TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text})

@app.route("/", methods=["GET", "POST"])
def checklist():
    if not os.path.exists(CHECKLIST_FILE):
        with open(CHECKLIST_FILE, "w") as f:
            json.dump(default_checklist, f)

    with open(CHECKLIST_FILE) as f:
        checklist = json.load(f)

    if request.method == "POST":
        for key in checklist:
            checklist[key] = key in request.form
        with open(CHECKLIST_FILE, "w") as f:
            json.dump(checklist, f)
        return redirect(url_for("checklist"))

    return render_template("checklist.html", checklist=checklist)

@app.route("/webhook", methods=["POST"])
def webhook():
    global TELEGRAM_CHAT_ID
    data = request.get_json()
    if "message" in data and "chat" in data["message"]:
        TELEGRAM_CHAT_ID = data["message"]["chat"]["id"]
        send_telegram_message("✅ Webhook успішно підключено!")
    return {"ok": True}

default_checklist = {
    "Ultra White": True,
    "Nitro Super Dry": True,
    "Nitro Cosmic Peach": True,
    "Ultra Peachy Keen": True,
    "Ultra Paradise": True,
    "Ultra Fiesta Mango": False,
    "Ultra Rosa": False,
    "Ultra Black": False,
    "Bad Apple": False,
    "Pipeline Punch": True,
    "Pacific Punch": False,
    "Juice Monarch": True,
    "Mango Loco": False,
    "Rio Fiesta": True,
    "Fanta Ruby Red": True
}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)