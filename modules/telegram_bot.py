import os
import requests

def send_telegram_alert(message):
    token = os.environ.get("SAMARITANA_BOT_TOKEN")
    chat_id = os.environ.get("SAMARITANA_CHAT_ID")
    if not token or not chat_id:
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": f"[SAMARITANA // ALERTA TÁTICO]\n{message}", "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
        return True
    except:
        return False

def check_telegram_commands():
    token = os.environ.get("SAMARITANA_BOT_TOKEN")
    if not token:
        return []
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            return res.json().get("result", [])
    except:
        pass
    return []
