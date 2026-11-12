from flask import Flask, render_template_string, jsonify, request, Response
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.scanner import run_scanner
from modules.iplookup import get_ip_info
from modules.netscanner import scan_local_network
from modules.cve_scanner import check_vulnerabilities
from modules.fim import check_integrity
from modules.hardening import generate_hardening_advice
from modules.honeypot import start_honeypot_listener
from modules.auditor import audit_dependencies
from modules.process_monitor import get_active_processes
from modules.netstat_monitor import get_active_connections
from modules.remediation import check_termux_environment, kill_process_by_pid
from database.storage import get_targets, save_target, get_scan_history, export_history_csv

app = Flask(__name__)

honeypot_logs = []
def log_honeypot(msg):
    honeypot_logs.append(msg)
start_honeypot_listener(log_callback=log_honeypot)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Samaritana OS // Elite Suite</title>
    <style>
        body { background-color: #050505; color: #ff3333; font-family: monospace; margin: 0; padding: 15px; }
        h1 { border-bottom: 2px solid #ff3333; padding-bottom: 8px; font-size: 1.1rem; }
        .card { background: #111; border: 1px solid #ff3333; padding: 12px; margin-bottom: 12px; border-radius: 4px; }
        input, select { background: #000; color: #00ffff; border: 1px solid #ff3333; padding: 8px; width: 100%; margin-bottom: 8px; font-family: monospace; box-sizing: border-box; }
        button { background: #ff3333; color: #000; border: none; padding: 10px; font-weight: bold; cursor: pointer; width: 100%; font-family: monospace; margin-bottom: 5px; }
        button:active { background: #cc0000; }
        pre { color: #00ffff; white-space: pre-wrap; word-wrap: break-word; font-size: 0.8rem; max-height: 220px; overflow-y: auto; }
        .status-bar { display: flex; justify-content: space-between; font-size: 0.8rem; color: #00ffff; margin-bottom: 10px; border: 1px dashed #ff3333; padding: 6px; }
    </style>
</head>
<body>
    <h1>SAMARITANA OS // ELITE SUITE</h1>
    
    <div class="status-bar">
        <span>STATUS: DEFESA ATIVA</span>
        <span>MODO: CYBER SECURITY</span>
    </div>

    <div class="card">
        <h3>GERENCIAR ALVOS & REDE</h3>
        <input type="text" id="newTarget" placeholder="Ex: 192.168.1.100">
        <button onclick="addTarget()">ADICIONAR ALVO</button>
        <select id="targetSelect"></select>
        <button onclick="triggerNetScan()" style="background:#00ffff; color:#000;">VARRER REDE WI-FI LOCAL</button>
    </div>

    <div class="card">
        <h3>VIGILÂNCIA, CVE & HARDENING</h3>
        <button onclick="triggerScan()">EXECUTAR SCAN + HARDENING</button>
        <input type="text" id="lookupIp" value="8.8.8.8" style="margin-top:8px;">
        <button onclick="triggerLookup()">CONSULTAR IP (GEO)</button>
    </div>

    <div class="card">
        <h3>SEGURANÇA DE SISTEMA (FIM & HONEYPOT)</h3>
        <button onclick="triggerFim()" style="background:#333; color:#00ffff; border:1px solid #00ffff;">VERIFICAR INTEGRIDADE (FIM)</button>
        <button onclick="triggerHoneypotLogs()" style="background:#333; color:#ffcc00; border:1px solid #ffcc00;">VER LOGS DO HONEYPOT</button>
    </div>

    <div class="card">
        <h3>DIAGNÓSTICO & REMEDIAÇÃO</h3>
        <button onclick="triggerEnvCheck()" style="background:#333; color:#ff00ff; border:1px solid #ff00ff;">AUTO-DIAGNÓSTICO DO AMBIENTE</button>
        <button onclick="triggerAudit()" style="background:#333; color:#00ff88; border:1px solid #00ff88;">AUDITAR DEPENDÊNCIAS PIP</button>
        <button onclick="triggerConnections()" style="background:#333; color:#00ffff; border:1px solid #00ffff;">MONITORAR SOCKETS / CONEXÕES</button>
        <input type="text" id="pidInput" placeholder="Digite o PID para matar processo" style="margin-top:8px;">
        <button onclick="triggerKillProcess()" style="background:#ff0055; color:#fff;">ENCERRAR PROCESSO (PID)</button>
    </div>

    <div class="card">
        <h3>RELATÓRIOS & HISTÓRICO</h3>
        <button onclick="loadHistory()" style="background:#333; color:#ff3333; border:1px solid #ff3333;">CARREGAR HISTÓRICO CRIPTOGRAFADO</button>
        <button onclick="window.location.href='/export_csv'" style="background:#00ff88; color:#000;">BAIXAR RELATÓRIO CSV</button>
        <pre id="output">Aguardando comando...</pre>
    </div>

    <script>
        function loadTargets() {
            fetch('/targets')
                .then(res => res.json())
                .then(data => {
                    let select = document.getElementById('targetSelect');
                    select.innerHTML = '';
                    data.forEach(t => {
                        let opt = document.createElement('option');
                        opt.value = t;
                        opt.textContent = t;
                        select.appendChild(opt);
                    });
                });
        }

        function addTarget() {
            let val = document.getElementById('newTarget').value;
            if(!val) return;
            fetch('/add_target', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({target: val})
            }).then(res => res.json()).then(data => {
                loadTargets();
                document.getElementById('output').innerText = "Alvo salvo: " + val;
            });
        }

        function triggerScan() {
            let target = document.getElementById('targetSelect').value || "127.0.0.1";
            document.getElementById('output').innerText = "Varredura e análise de hardening em andamento para " + target + "...";
            fetch('/scan?target=' + target)
                .then(res => res.json())
                .then(data => {
                    document.getElementById('output').innerText = JSON.stringify(data, null, 2);
                });
        }

        function triggerNetScan() {
            document.getElementById('output').innerText = "Varredura ARP da rede local em andamento...";
            fetch('/netscan')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('output').innerText = JSON.stringify(data, null, 2);
                });
        }

        function triggerLookup() {
            let ip = document.getElementById('lookupIp').value;
            document.getElementById('output').innerText = "Consultando IP " + ip + "...";
            fetch('/lookup?ip=' + ip)
                .then(res => res.json())
                .then(data => {
                    document.getElementById('output').innerText = JSON.stringify(data, null, 2);
                });
        }

        function triggerFim() {
            document.getElementById('output').innerText = "Verificando integridade dos arquivos do sistema...";
            fetch('/fim')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('output').innerText = JSON.stringify(data, null, 2);
                });
        }

        function triggerHoneypotLogs() {
            document.getElementById('output').innerText = "Buscando alertas do Honeypot (com persistência local)...";
            fetch('/honeypot_logs')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('output').innerText = JSON.stringify(data, null, 2);
                });
        }

        function triggerAudit() {
            document.getElementById('output').innerText = "Auditando pacotes Python instalados...";
            fetch('/audit')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('output').innerText = JSON.stringify(data, null, 2);
                });
        }

        function triggerEnvCheck() {
            document.getElementById('output').innerText = "Verificando dependências do sistema Termux...";
            fetch('/env_check')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('output').innerText = JSON.stringify(data, null, 2);
                });
        }

        function triggerConnections() {
            document.getElementById('output').innerText = "Analisando conexões de rede e sockets ativos...";
            fetch('/connections')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('output').innerText = JSON.stringify(data, null, 2);
                });
        }

        function triggerKillProcess() {
            let pid = document.getElementById('pidInput').value;
            if(!pid) { alert("Insira um PID válido"); return; }
            document.getElementById('output').innerText = "Encerrando processo PID " + pid + "...";
            fetch('/kill_process?pid=' + pid)
                .then(res => res.json())
                .then(data => {
                    document.getElementById('output').innerText = JSON.stringify(data, null, 2);
                });
        }

        function loadHistory() {
            document.getElementById('output').innerText = "Descriptografando histórico completo de logs...";
            fetch('/history')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('output').innerText = JSON.stringify(data, null, 2);
                });
        }

        loadTargets();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/targets')
def targets_route():
    return jsonify(get_targets())

@app.route('/add_target', methods=['POST'])
def add_target_route():
    data = request.get_json()
    target = data.get("target")
    if target:
        save_target(target)
    return jsonify({"status": "success", "targets": get_targets()})

@app.route('/scan')
def scan():
    target = request.args.get('target', '127.0.0.1')
    results = run_scanner(target, ports=[21, 22, 80, 443, 3000, 8080])
    for res in results:
        banner = res.get("banner", "")
        if banner:
            res["cve_analysis"] = check_vulnerabilities(banner)
    hardening = generate_hardening_advice(results)
    return jsonify({"scan_results": results, "hardening_recommendations": hardening})

@app.route('/netscan')
def netscan():
    return jsonify(scan_local_network())

@app.route('/lookup')
def lookup():
    ip = request.args.get('ip', '8.8.8.8')
    return jsonify(get_ip_info(ip))

@app.route('/fim')
def fim():
    return jsonify(check_integrity())

@app.route('/honeypot_logs')
def hp_logs():
    return jsonify({"honeypot_port": 9999, "live_alerts": honeypot_logs, "encrypted_history": get_scan_history()})

@app.route('/audit')
def audit_route():
    return jsonify(audit_dependencies())

@app.route('/env_check')
def env_check_route():
    return jsonify(check_termux_environment())

@app.route('/connections')
def connections_route():
    return jsonify(get_active_connections())

@app.route('/kill_process')
def kill_process_route():
    pid = request.args.get('pid')
    return jsonify(kill_process_by_pid(pid))

@app.route('/history')
def history():
    return jsonify(get_scan_history())

@app.route('/export_csv')
def export_csv():
    csv_data = export_history_csv()
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=samaritana_report.csv"}
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
