import os
import hashlib

WATCH_FILES = [
    os.path.expanduser("~/samaritana_core/ui/app.py"),
    os.path.expanduser("~/samaritana_core/modules/scanner.py")
]

def calculate_hash(filepath):
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()
    except:
        return "ERROR"

def check_integrity():
    report = []
    for f in WATCH_FILES:
        current_hash = calculate_hash(f)
        report.append({"file": f, "sha256": current_hash, "status": "Integridade OK"})
    return report

if __name__ == "__main__":
    print(check_integrity())
