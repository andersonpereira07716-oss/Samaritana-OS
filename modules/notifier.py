import requests
import os

TELEGRAM_BOT_TOKEN = os.getenv("SAMARITANA_BOT_TOKEN", "SEU_BOT_TOKEN_AQUI")
TELEGRAM_CHAT_ID = os.getenv("SAMARITANA_CHAT_ID", "SEU_CHAT_ID_AQUI")

def send_telegram_alert(message):
    if TELEGRAM_BOT_TOKEN == "SEU_BOT_TOKEN_AQUI" or not TELEGRAM_BOT_TOKEN:
        print("\033[91m[SAMARITANA // ALERTA] Token do Telegram não configurado.\033[0m")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"🔴 [SAMARITANA // RELATÓRIO DE VIGILÂNCIA]\n\n{message}",
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("\033[96m[SAMARITANA // NOTIFIER] Alerta transmitido com sucesso via Telegram.\033[0m")
            return True
        else:
            print(f"\033[91m[SAMARITANA // ERRO] Falha ao enviar alerta: {response.text}\033[0m")
            return False
    except Exception as e:
        print(f"\033[91m[SAMARITANA // ERRO] Exceção de rede: {e}\033[0m")
        return False

if __name__ == "__main__":
    print("Módulo de notificação da Samaritana carregado.")
