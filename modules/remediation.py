import subprocess
import os

def check_termux_environment():
    tools = ['nmap', 'python', 'pip', 'netstat', 'ss', 'ps']
    status = {}
    for tool in tools:
        res = subprocess.run(f"command -v {tool}", shell=True, capture_output=True, text=True)
        status[tool] = "Disponível" if res.returncode == 0 else "Ausente/Não instalado"
    return {"status": "success", "environment_check": status}

def kill_process_by_pid(pid):
    try:
        os.kill(int(pid), 9)
        return {"status": "success", "message": f"Processo PID {pid} encerrado com sucesso."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
