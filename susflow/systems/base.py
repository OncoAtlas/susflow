# susflow/systems/base.py
from pathlib import Path
import polars as pl
from .. import ftp as _ftp
from ..parsers import converter as _converter
from ..storage import local_lake as _lake

def generic_load(
    system: str, 
    sub_dir: str, 
    table: str, 
    uf: str, 
    year: int, 
    month: int = 0, 
    use_polars: bool = True
):
    """
    Motor universal de carga de dados do DATASUS.
    Gerencia o fluxo: Verificação de Cache -> Download FTP -> Conversão Parquet -> Leitura.
    """
    # 1. Define o destino único no Lake (Cache)
    parquet_path = _lake.get_path(system, table, year, month, uf)
    
    if not parquet_path.exists():
        # 2. Preparação dos componentes do nome do arquivo
        yy = str(year)[-2:]
        mm = str(month).zfill(2)
        
        # Define se o sufixo é mensal (YYMM) ou anual (YYYY)
        # CNES/SIH/SIA usam YYMM. SIM/SINASC/SINAN usam o ano.
        date_suffix = f"{yy}{mm}" if month > 0 else str(year)
        nome_arquivo = f"{table.upper()}{uf.upper()}{date_suffix}.dbc"
        
        # 3. Montagem da URL do FTP (Onde moram as exceções)
        # Regra Geral: /system/sub_dir/TABLE/arquivo.dbc
        caminho_ftp = f"/dissemin/publicos/{system}/{sub_dir}/{nome_arquivo}"

        
        # Exceção conhecida: O SIM (DORES) não usa subpasta para a tabela
        if system in ["SIM", "SINASC"]:
            caminho_ftp = f"/dissemin/publicos/{system}/{sub_dir}/{nome_arquivo}"

        temp_dbc = _lake.get_temp_path(nome_arquivo)
        
        try:
            print(f"📥 [{system}] Baixando {nome_arquivo}...")
            _ftp.baixar(caminho_ftp, temp_dbc)
            
            print(f"⚙️ [{system}] Convertendo para Parquet...")
            _converter.to_parquet(temp_dbc, parquet_path)
            
        except Exception as e:
            # Limpa o arquivo parcial em caso de erro na conversão ou download
            if parquet_path.exists():
                parquet_path.unlink()
            raise Exception(f"Falha ao processar {system} {table}: {e}")
        finally:
            # Sempre limpa o arquivo .dbc temporário
            if temp_dbc.exists():
                temp_dbc.unlink()

    # 4. Retorna o DataFrame (do cache ou recém-convertido)
    return _converter.load_as_df(parquet_path, use_polars=use_polars)