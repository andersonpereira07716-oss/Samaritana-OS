def check_vulnerabilities(banner_text):
    banner = banner_text.lower()
    vulns = []
    
    # Base simples e direta de regras de CVE para serviços comuns
    if "vsftpd 2.3.4" in banner:
        vulns.append({"cve": "CVE-2011-2523", "severity": "CRITICAL", "desc": "Backdoor de execução remota de código no vsftpd 2.3.4."})
    if "openssh 4." in banner or "openssh 5." in banner:
        vulns.append({"cve": "CVE-2008-0166", "severity": "HIGH", "desc": "Fraqueza na geração de chaves em versões antigas do OpenSSH."})
    if "apache/2.2" in banner or "apache/2.0" in banner:
        vulns.append({"cve": "CVE-2012-0053", "severity": "MEDIUM", "desc": "Vazamento de informações via reescrita HTTP em servidores Apache antigos."})
    
    if not vulns and banner.strip():
        vulns.append({"cve": "N/A", "severity": "LOW", "desc": "Nenhuma vulnerabilidade crítica conhecida identificada no banner atual."})
        
    return vulns

if __name__ == "__main__":
    print(check_vulnerabilities("vsftpd 2.3.4"))
