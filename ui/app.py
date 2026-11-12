from flask import Flask, render_template_string, jsonify
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.reporter import generate_audit_report

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Samaritana OS // Command Center</title>
    <style>
        body { background-color: #030303; color: #00ffcc; font-family: 'Courier New', monospace; margin: 0; padding: 15px; }
        .container { max-width: 600px; margin: auto; }
        h1 { color: #ff0055; text-shadow: 0 0 10px #ff0055; text-align: center; font-size: 1.5rem; }
        .card { background: #0a0a0a; border: 1px solid #00ffcc; padding: 15px; margin-bottom: 15px; border-radius: 6px; box-shadow: 0 0 10px rgba(0,255,204,0.1); }
        .btn { display: block; width: 100%; background: #ff0055; color: #fff; border: none; padding: 14px; font-size: 1rem; font-weight: bold; border-radius: 4px; cursor: pointer; text-align: center; text-transform: uppercase; margin-top: 10px; box-shadow: 0 0 10px #ff0055; }
        .btn:active { background: #cc0044; }
        .status-ok { color: #00ff66; }
    </style>
</head>
<body>
    <div class="container">
        <h1>SAMARITANA OS</h1>
        <div class="card">
            <h3>STATUS DO NÚCLEO</h3>
            <p>Daemon: <span class="status-ok">● ONLINE (PROTECTED)</span></p>
            <p>Blindagem: PyArmor + Fernet</p>
            <p>Canal Telegram: Ativo</p>
        </div>
        <div class="card">
            <h3>AÇÕES TÁTICAS</h3>
            <button class="btn" onclick="runAudit()">Gerar Laudo Executivo</button>
            <div id="result" style="margin-top: 10px; font-size: 0.9rem; color: #00ffcc;"></div>
        </div>
    </div>
    <script>
        function runAudit() {
            document.getElementById('result').innerText = "[*] Executando varredura e gerando laudo...";
            fetch('/api/audit')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('result').innerText = "[+] Sucesso! Laudo gerado em " + data.file;
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(TEMPLATE)

@app.route('/api/audit')
def api_audit():
    generate_audit_report()
    return jsonify({"status": "success", "file": "reports/"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
