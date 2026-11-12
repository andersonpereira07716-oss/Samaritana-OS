import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.scanner import run_scanner

def start_daemon(target="127.0.0.1", interval=300):
    print(f"\033[91m[SAMARITANA // DAEMON] Iniciando vigilância contínua em segundo plano (Alvo: {target}, Intervalo: {interval}s)...\033[0m")
    try:
        while True:
            run_scanner(target_ip=target, ports=[21, 22, 80, 443, 3000, 8080])
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\033[91m[SAMARITANA // DAEMON] Vigilância contínua encerrada.\033[0m")

if __name__ == "__main__":
    target_ip = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    start_daemon(target=target_ip)
