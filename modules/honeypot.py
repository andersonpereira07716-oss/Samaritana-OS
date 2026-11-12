import socket
import threading
import os
import sys
import json
from cryptography.fernet import Fernet

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../database/scans.enc'))
KEY_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../database/secret.key'))

def _get_fernet():
    try:
        if os.path.exists(KEY_PATH):
            with open(KEY_PATH, 'rb') as f:
                key = f.read()
            return Fernet(key)
    except:
        pass
    return None

def save_honeypot_alert(alert_data):
    try:
        f = _get_fernet()
        data = []
        if os.path.exists(DB_PATH) and f:
            with open(DB_PATH, 'rb') as file:
                decrypted = f.decrypt(file.read())
                data = json.loads(decrypted.decode())
        
        data.append(alert_data)
        
        if f:
            encrypted = f.encrypt(json.dumps(data).encode())
            with open(DB_PATH, 'wb') as file:
                file.write(encrypted)
    except Exception as e:
        print(f"Erro ao salvar no banco criptografado: {e}")

def honeypot_worker(log_callback):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(('0.0.0.0', 9999))
        server.listen(5)
        while True:
            client, addr = server.accept()
            msg = f"[ALERTA HONEYPOT] Conexão detectada de {addr[0]}:{addr[1]}"
            if log_callback:
                log_callback(msg)
            
            # Salva de forma segura no cofre encriptado
            save_honeypot_alert({"target": "honeypot", "alert": msg, "source_ip": addr[0]})
            
            try:
                client.send(b"WARNING: UNAUTHORIZED ACCESS LOGGED BY SAMARITANA OS\n")
                client.close()
            except:
                pass
    except Exception as e:
        if log_callback:
            log_callback(f"[ERRO HONEYPOT] Porta 9999 indisponível: {e}")

def start_honeypot_listener(log_callback=None):
    t = threading.Thread(target=honeypot_worker, args=(log_callback,), daemon=True)
    t.start()
