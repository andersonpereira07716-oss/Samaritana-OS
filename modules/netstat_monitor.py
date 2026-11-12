import subprocess

def get_active_connections():
    try:
        # Tenta listar conexões de rede ativas no ambiente
        result = subprocess.run(['netstat', '-an'], capture_output=True, text=True)
        if result.returncode != 0:
            # Fallback caso netstat não esteja disponível
            result = subprocess.run(['ss', '-tunap'], capture_output=True, text=True)
        
        lines = result.stdout.splitlines()
        connections = [line for line in lines if 'ESTABLISHED' in line or 'LISTEN' in line]
        return {"status": "success", "connections": connections if connections else lines[:15]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    print(get_active_connections())
