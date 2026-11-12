import os
import json
import time
from datetime import datetime

def generate_audit_report(target="127.0.0.1", risk_score=15):
    report_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target": target,
        "risk_score": risk_score,
        "status": "SECURE" if risk_score < 50 else "CRITICAL_ALERT",
        "modules_active": [
            "honeypot", "fim", "cve_scanner", "netstat_monitor", 
            "remediation", "telegram_bot", "storage", "license_check"
        ],
        "recommendations": [
            "Maintain PyArmor runtime obfuscation active.",
            "Verify Telegram bot webhook connectivity.",
            "Inspect encrypted FIM databases periodically."
        ]
    }
    
    filename = f"reports/audit_report_{int(time.time())}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4)
        
    html_filename = filename.replace(".json", ".html")
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Samaritana OS - Laudo Executivo</title>
    <style>
        body {{ background: #050505; color: #00ffcc; font-family: monospace; padding: 20px; }}
        .card {{ border: 1px solid #00ffcc; padding: 20px; border-radius: 8px; background: #111; max-width: 600px; margin: auto; }}
        h1 {{ color: #ff0055; text-shadow: 0 0 10px #ff0055; }}
        .risk {{ font-size: 24px; color: {'#00ffcc' if risk_score < 50 else '#ff0055'}; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>SAMARITANA OS // LAUDO TÉCNICO</h1>
        <p><b>Data:</b> {report_data['timestamp']}</p>
        <p><b>Alvo Auditado:</b> {target}</p>
        <p class="risk">Score de Risco: {risk_score}/100</p>
        <p><b>Status do Sistema:</b> {report_data['status']}</p>
        <h3>Módulos Ativos:</h3>
        <ul>{"".join([f"<li>{m}</li>" for m in report_data['modules_active']])}</ul>
    </div>
</body>
</html>
"""
    with open(html_filename, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"[+] Relatório gerado com sucesso: {html_filename}")
if __name__ == "__main__":
    generate_audit_report()
