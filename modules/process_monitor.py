import subprocess

def get_active_processes():
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        python_processes = [line for line in lines if 'python' in line.lower()]
        return {"status": "success", "active_python_processes": python_processes}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    print(get_active_processes())
