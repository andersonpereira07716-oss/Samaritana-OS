import os
from cryptography.fernet import Fernet
import json
from datetime import datetime
import csv
import io

KEY_FILE = os.path.expanduser("~/samaritana_core/database/secret.key")
DATA_FILE = os.path.expanduser("~/samaritana_core/database/scans.enc")
TARGETS_FILE = os.path.expanduser("~/samaritana_core/database/targets.json")

def load_or_create_key():
    if not os.path.exists(KEY_FILE):
        os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return key

def save_encrypted_scan(target, results):
    key = load_or_create_key()
    fernet = Fernet(key)
    
    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target": target,
        "results": results
    }
    
    data_list = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "rb") as f:
                decrypted_data = fernet.decrypt(f.read())
                data_list = json.loads(decrypted_data.decode())
        except:
            data_list = []
            
    data_list.append(record)
    encrypted_data = fernet.encrypt(json.dumps(data_list).encode())
    
    with open(DATA_FILE, "wb") as f:
        f.write(encrypted_data)

def get_scan_history():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        key = load_or_create_key()
        fernet = Fernet(key)
        with open(DATA_FILE, "rb") as f:
            decrypted_data = fernet.decrypt(f.read())
            return json.loads(decrypted_data.decode())
    except:
        return []

def export_history_csv():
    history = get_scan_history()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Timestamp", "Target", "Port", "Status", "Banner"])
    
    for item in history:
        ts = item.get("timestamp")
        target = item.get("target")
        for res in item.get("results", []):
            port = res.get("port")
            status = res.get("status")
            banner = res.get("banner", "")
            writer.writerow([ts, target, port, status, banner])
            
    return output.getvalue()

def get_targets():
    if os.path.exists(TARGETS_FILE):
        with open(TARGETS_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                pass
    return ["127.0.0.1"]

def save_target(target):
    targets = get_targets()
    if target not in targets:
        targets.append(target)
        os.makedirs(os.path.dirname(TARGETS_FILE), exist_ok=True)
        with open(TARGETS_FILE, "w") as f:
            json.dump(targets, f)
    return targets
