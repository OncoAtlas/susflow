# test_drive.py
from susflow.systems import cnes

print("🔍 Testando a inteligência do Backtracking...")

try:
    # Testando com a tabela de Equipamentos (EQ) na Paraíba
    # Não passamos data, a lib vai 'caçar' o dado no FTP
    df_eq = cnes.load_latest(table="EQ", uf="PB")
    
    print(f"\n✅ Sucesso! Tabela EQ carregada.")
    print(f"Shape: {df_eq.shape}")
    
    # Verificando se os dados são recentes
    if "COMPETEN" in df_eq.columns:
        print(f"Competência dos dados: {df_eq['COMPETEN'].unique().to_list()}")

except Exception as e:
    print(f"\n❌ Falha no teste: {e}")