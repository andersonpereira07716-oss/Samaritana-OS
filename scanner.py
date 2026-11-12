import socket
import concurrent.futures
from datetime import datetime

# Cores de Estética Cyberpunk (Vermelho Samaritana / Alerta)
COLOR_RED = "\033[91m"
COLOR_CYAN = "\033[96m"
COLOR_YELLOW = "\033[93m"
COLOR_RESET = "\033[0m"

def scan_port(target_ip, port):
    """Tenta estabelecer uma conexão TCP com a porta especificada."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        result = sock.connect_ex((target_ip, port))
        sock.close()
        if result == 0:
            return port
    except Exception:
        pass
    return None

def run_scanner(target_ip="127.0.0.1", ports=range(1, 1025), max_threads=100):
    """Executa a varredura multithreaded nas portas selecionadas."""
    print(f"\n{COLOR_RED}[SAMARITANA // SCANNER] Iniciando varredura em {target_ip}...{COLOR_RESET}")
    print(f"{COLOR_CYAN}[INFO] Alvos: {len(ports)} portas | Threads simultâneas: {max_threads}{COLOR_RESET}\n")
    
    start_time = datetime.now()
    open_ports = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(scan_port, target_ip, port): port for port in ports}
        
        for future in concurrent.futures.as_completed(futures):
            port = future.result()
            if port:
                print(f"{COLOR_YELLOW}[+] PORTA ABERTA DETECTADA: {port}{COLOR_RESET}")
                open_ports.append(port)

    elapsed = datetime.now() - start_time
    print(f"\n{COLOR_RED}[SAMARITANA // SCANNER] Varredura finalizada em {elapsed.total_seconds():.2f}s.{COLOR_RESET}")
    print(f"{COLOR_CYAN}[RESUMO] Portas abertas encontradas: {open_ports if open_ports else 'Nenhuma'}{COLOR_RESET}\n")
    return open_ports

if __name__ == "__main__":
    # Teste local padrão (Loopback) ou IP de destino configurável
    target = input(f"{COLOR_CYAN}Digite o IP alvo para varredura (Padrão: 127.0.0.1): {COLOR_RESET}").strip()
    if not target:
        target = "127.0.0.1"
    run_scanner(target_ip=target)
