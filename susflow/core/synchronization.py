# susflow/core/synchronization.py
from datetime import date
from .. import ftp as _ftp

class BacktrackingEngine:
    def __init__(self, system: str = "CNES", max_months: int = 12):
        self.system = system
        self.max_months = max_months

    def find_latest_consistent(self, tables: list, uf: str):
        """
        Returns the (year, month) of the most recent period where ALL
        tables in the list exist on the FTP.
        """
        hoje = date.today()
        ano_atual = hoje.year
        mes_atual = hoje.month

        for i in range(self.max_months):
            # Calculates the target month backward
            m_idx = (mes_atual - i - 1) % 12 + 1
            y_idx = ano_atual - ((i + (12 - mes_atual)) // 12)
            
            yy = str(y_idx)[-2:]
            mm = str(m_idx).zfill(2)
            
            consistente = True
            for table in tables:
                # Build the generic path based on the system
                nome_arq = f"{table.upper()}{uf.upper()}{yy}{mm}.dbc"
                path_ftp = f"/dissemin/publicos/{self.system}/200508_/Dados/{table.upper()}/{nome_arq}"
                
                if not _ftp.existe(path_ftp):
                    consistente = False
                    break
            
            if consistente:
                return y_idx, m_idx
                
        raise FileNotFoundError(f"Nenhum mês consistente encontrado para {tables} nos últimos {self.max_months} meses.")