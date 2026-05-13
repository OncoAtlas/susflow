# debug_ftp.py
from susflow import ftp

print("📂 Explorando o diretório do SINASC...")
try:
    # 1. Listar a raiz do SINASC
    print(f"Raiz: {ftp.listar('/dissemin/publicos/SINASC')}")
    
    # 2. Listar o que tem dentro de 1996_/ (Pode ser Dados ou DADOS ou DN)
    print(f"Sub-1996: {ftp.listar('/dissemin/publicos/SINASC/1996_')}")
    
    # 3. Tentar achar a pasta final
    # Vamos testar variações comuns do DATASUS
    for pasta in ["Dados/DN", "DADOS/DN", "Dados", "DN"]:
        try:
            arquivos = ftp.listar(f"/dissemin/publicos/SINASC/1996_/{pasta}")
            print(f"✅ Achei em '{pasta}': {arquivos[:3]}... (Total: {len(arquivos)})")
        except:
            print(f"❌ Não existe: 1996_/{pasta}")

except Exception as e:
    print(f"💥 Erro na exploração: {e}")