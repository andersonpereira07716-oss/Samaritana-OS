import os
import time
import sys
from datetime import datetime

# Configuração de Cores para o Terminal (Estilo Samaritana - Alerta/Vermelho ou Frio)
COLOR_RED = "\033[91m"
COLOR_CYAN = "\033[96m"
COLOR_RESET = "\033[0m"

def log_system(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    color = COLOR_RED if level == "ALERT" else COLOR_CYAN
    print(f"{color}[SAMARITANA // {level}] {timestamp} - {message}{COLOR_RESET}")

def boot_sequence():
    os.system("clear")
    print(f"{COLOR_RED}==================================================")
    print("       SAMARITANA OS - INITIALIZING CORE          ")
    print(f"=================================================={COLOR_RESET}")
    time.sleep(1)
    
    steps = [
        "Carregando matrizes de vigilância distribuída...",
        "Estabelecendo conexão com nós locais (Termux Environment)...",
        "Ativando protocolos de varredura e interceptação...",
        "Sistemas operacionais. Vigilância ativa."
    ]
    
    for step in steps:
        log_system(step, "INIT")
        time.sleep(0.8)

if __name__ == "__main__":
    boot_sequence()
    try:
        while True:
            log_system("Varredura de rotina concluída. Nenhuma anomalia crítica.", "STATUS")
            time.sleep(5)
    except KeyboardInterrupt:
        log_system("Desligamento manual acionado pelo operador.", "ALERT")
        sys.exit(0)
