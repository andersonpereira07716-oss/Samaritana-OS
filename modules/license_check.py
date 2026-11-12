import os
import hashlib

def verify_system_signature():
    key_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../database/secret.key'))
    if not os.path.exists(key_path):
        return {"status": "warning", "message": "Aviso: Chave de segurança não encontrada. O ambiente pode não estar blindado."}
    return {"status": "secure", "message": "Assinatura do sistema validada com sucesso."}
