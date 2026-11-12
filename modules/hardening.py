def generate_hardening_advice(scan_results):
    advice = []
    for res in scan_results:
        port = res.get("port")
        banner = res.get("banner", "").lower()
        
        if port == 21:
            advice.append("Porta FTP (21) aberta: Recomenda-se desativar o serviço ou migrar para SFTP (porta 22) para evitar ataques de força bruta em texto plano.")
        elif port == 22:
            advice.append("Porta SSH (22) aberta: Certifique-se de desabilitar a autenticação por senha no sshd_config e utilizar apenas chaves públicas.")
        elif port in [80, 443, 3000, 8080]:
            advice.append(f"Serviço Web detectado na porta {port}: Verifique se há cabeçalhos de segurança ativos e evite expor endpoints de administração sem autenticação.")
            
    if not advice:
        advice.append("Nenhum risco óbvio detectado nos serviços mapeados. Mantenham-se as regras atuais de firewall.")
        
    return advice

if __name__ == "__main__":
    print(generate_hardening_advice([]))
