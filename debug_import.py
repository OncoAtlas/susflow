import sys
from pathlib import Path

# Força o Python a olhar para a pasta atual antes de qualquer pacote instalado
sys.path.insert(0, str(Path.cwd()))

print("--- Debug de Caminhos ---")
try:
    from susflow.storage import local_lake
    print("✅ Sucesso ao importar local_lake")
    
    from susflow.parsers import converter
    print("✅ Sucesso ao importar converter")
    
    from susflow.systems import cnes
    print("✅ Sucesso ao importar cnes")
    
except ImportError as e:
    print(f"❌ Erro de Importação: {e}")
    # Isso vai nos dizer exatamente qual arquivo está disparando o erro
    import traceback
    traceback.print_exc()