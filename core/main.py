import os
import sys
import time
from datetime import datetime

# Adiciona a raiz do projeto ao path para permitir imports dos módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.scanner import run_scanner
from database.storage import load_or_create_key, read_encrypted_scan

# Cores de Estética Cyberpunk (Vermelho Samaritana / Alerta)
COLOR_RED = "\033[91m"
COLOR_CYAN = "\033[96m"
COLOR_YELLOW = "\033[93m"
COLOR_RESET = "\033[0m"

DB_DIR = os.path.expanduser("~/samaritana_core/database/")

def clear_screen():
    os.system("clear")

def banner():
    print(f"{COLOR_RED}==================================================")
    print("         SAMARITANA OS // CORE CONTROL            ")
    print(f"=================================================={COLOR_RESET}")
    print(f"{COLOR_CYAN} Operador: Anderson // Ambiente: Termux Android   {COLOR_RESET}")
    print(f"{COLOR_RED}--------------------------------------------------{COLOR_RESET}")

def list_stored_logs():
    clear_screen()
    banner()
    print(f"\n{COLOR_YELLOW}[GESTOR DE REGISTROS // BANCO DE DADOS]{COLOR_RESET}")
    if not os.path.exists(DB_DIR):
        print(f"{COLOR_RED}Nenhum banco de dados encontrado.{COLOR_RESET}")
        input(f"\nPressione ENTER para voltar ao menu...")
        return

    files = [f for f in os.listdir(DB_DIR) if f.endswith(".enc")]
    if not files:
        print(f"{COLOR_CYAN}Nenhum relatório criptografado encontrado na base.{COLOR_RESET}")
        input(f"\nPressione ENTER para voltar ao menu...")
        return

    print(f"\nRelatórios disponíveis ({len(files)}):")
    for idx, file in enumerate(files, 1):
        print(f" [{idx}] {file}")

    choice = input(f"\n{COLOR_CYAN}Digite o número do relatório para descriptografar (ou 0 para voltar): {COLOR_RESET}").strip()
    if choice.isdigit():
        idx = int(choice)
        if 1 <= idx <= len(files):
            target_file = os.path.join(DB_DIR, files[idx - 1])
            try:
                data = read_encrypted_scan(target_file)
                print(f"\n{COLOR_RED}=== DADOS DESCRIPTOGRAFADOS ==={COLOR_RESET}")
                print(f" Timestamp: {data.get('timestamp')}")
                print(f" Alvo:      {data.get('target')}")
                print(f" Portas:    {data.get('open_ports')}")
                print(f"{COLOR_RED}================================{COLOR_RESET}")
            except Exception as e:
                print(f"{COLOR_RED}[ERRO] Falha ao descriptografar: {e}{COLOR_RESET}")
            input(f"\nPressione ENTER para continuar...")

def main_menu():
    while True:
        clear_screen()
        banner()
        print(f"\n{COLOR_CYAN}[MENU PRINCIPAL]{COLOR_RESET}")
        print(" [1] Executar Varredura de Rede (Port Scanner)")
        print(" [2] Consultar Registros Criptografados (Database)")
        print(" [3] Status do Sistema / Teste de Núcleo")
        print(" [0] Desligar Sistema")
        
        choice = input(f"\n{COLOR_RED}samaritana@core ~ $ {COLOR_RESET}").strip()
        
        if choice == "1":
            clear_screen()
            target = input(f"{COLOR_CYAN}Digite o IP alvo para varredura (Padrão 127.0.0.1): {COLOR_RESET}").strip()
            if not target:
                target = "127.0.0.1"
            run_scanner(target_ip=target)
            input(f"\nPressione ENTER para voltar ao menu...")
        elif choice == "2":
            list_stored_logs()
        elif choice == "3":
            clear_screen()
            banner()
            print(f"\n{COLOR_CYAN}[DIAGNÓSTICO DO NÚCLEO]{COLOR_RESET}")
            print(f" - Chave de Criptografia: {'Ativa' if os.path.exists(os.path.join(DB_DIR, 'secret.key')) else 'Pendente'}")
            print(f" - Diretório de Logs: {DB_DIR}")
            print(f" - Status: Operacional em alta performance.")
            input(f"\nPressione ENTER para voltar ao menu...")
        elif choice == "0":
            print(f"\n{COLOR_RED}[SAMARITANA] Encerrando processos de vigilância. Até logo.{COLOR_RESET}")
            break
        else:
            print(f"{COLOR_RED}Opção inválida.{COLOR_RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{COLOR_RED}[ALERTA] Interrupção forçada pelo operador.{COLOR_RESET}")
        sys.exit(0)
