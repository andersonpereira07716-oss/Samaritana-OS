import socket
import concurrent.futures
from datetime import datetime
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from database.storage import save_encrypted_scan
except ImportError:
    save_encrypted_scan = None

try:
    from modules.notifier import send_telegram_alert
except ImportError:
    send_telegram_alert = None

COLOR_RED = "\033[91m"
COLOR_CYAN = "\033[96m"
COLOR_YELLOW = "\033[93m"
COLOR_RESET = "\033[0m"

def grab_banner(target_ip, port):
    try:
        s = socket.socket()
        s.settimeout(1.5)
        s.connect((target_ip, port))
        try:
            banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
        except:
            banner = "Desconhecido / Sem Banner"
        s.close()
        return banner if banner else "Serviço Ativo"
    except:
        return "Protegido / Sem Resposta"

def scan_port(target_ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        result = sock.connect_ex((target_ip, port))
        sock.close()
        if result == 0:
            banner = grab_banner(target_ip, port)
            return port, banner
    except Exception:
        pass
    return None

def run_scanner(target_ip="127.0.0.1", ports=range(1, 1025), max_threads=100):
    print(f"\n{COLOR_RED}[SAMARITANA // SCANNER + BANNER] Iniciando varredura em {target_ip}...{COLOR_RESET}")
    start_time = datetime.now()
    open_ports_info = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(scan_port, target_ip, port): port for port in ports}
        
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                port, banner = res
                print(f"{COLOR_YELLOW}[+] PORTA ABERTA: {port} | Serviço: {banner}{COLOR_RESET}")
                open_ports_info[str(port)] = banner

    elapsed = datetime.now() - start_time
    print(f"\n{COLOR_RED}[SAMARITANA // SCANNER] Finalizado em {elapsed.total_seconds():.2f}s.{COLOR_RESET}")
    
    if save_encrypted_scan:
        save_encrypted_scan(target_ip, open_ports_info)
        
    if open_ports_info and send_telegram_alert:
        alert_msg = f"Alvo: {target_ip}\nPortas e Serviços:\n{open_ports_info}\nStatus: Vigilância concluída."
        send_telegram_alert(alert_msg)
        
    return open_ports_info

if __name__ == "__main__":
    run_scanner()
