import subprocess
import socket

def scan_local_network():
    devices = []
    # Varredura simples baseada em ping na subnet local padrão do Termux/Wi-Fi
    base_ip = "192.168.1."
    for i in range(1, 255):
        ip = base_ip + str(i)
        # Executa um ping rápido de 1 pacote com timeout de 0.2s
        response = subprocess.run(['ping', '-c', '1', '-W', '1', ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if response.returncode == 0:
            devices.append({"ip": ip, "status": "Ativo"})
    return devices

if __name__ == "__main__":
    print(scan_local_network())
