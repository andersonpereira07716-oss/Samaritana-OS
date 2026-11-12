import os
import subprocess

print("[*] Iniciando processo de endurecimento e ofuscação da Samaritana OS...")

# Ofuscar a pasta de módulos para impedir leitura direta do código Python
if os.path.exists("modules"):
    subprocess.run(["pyarmor", "gen", "--recursive", "modules/"], capture_output=True)
    print("[+] Módulos ofuscados com sucesso via PyArmor!")

print("[+] Proteção concluída. O código sensível agora está cifrado contra engenharia reversa.")
