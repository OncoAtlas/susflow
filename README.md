# susflow

Biblioteca Python para acesso e download dos dados abertos do DATASUS. Abstrai o protocolo FTP, a descompressão dos arquivos `.dbc` e a leitura dos dados, entregando um DataFrame pronto para análise.

---

## Instalação

```bash
git clone https://github.com/seu-usuario/susflow.git
cd susflow
pip install -e .
```

Dependências: `pandas`, `pyreaddbc`, `dbfread`

---

## Como usar

### SINASC — Nascidos Vivos

```python
from susflow.systems import sinasc

# listar arquivos disponíveis no FTP
sinasc.listar()           # todos
sinasc.listar(uf="SP")    # filtrado por UF

# baixar para o cache (~/.susflow/cache/)
path = sinasc.baixar(uf="SP", ano=2022)

# baixar para pasta específica
path = sinasc.baixar(uf="SP", ano=2022, destino="/meus/dados")

# ler direto como DataFrame (baixa se necessário)
df = sinasc.ler(uf="SP", ano=2022)

# forçar novo download mesmo com cache
df = sinasc.ler(uf="SP", ano=2022, forcar=True)
```

### SIM — Mortalidade

```python
from susflow.systems import sim

# dados por UF
df = sim.ler(uf="SP", ano=2023)

# dados nacionais por categoria (DOFET)
# tipos disponíveis: EXT (causas externas), FET (fetal), INF (infantil), MAT (materno)
df = sim.ler_especial(tipo="EXT", ano=2024)
df = sim.ler_especial(tipo="MAT", ano=2022)

# listar
sim.listar(uf="RJ")
sim.listar_especial(tipo="INF")
```

### SINAN — Agravos de Notificação

```python
from susflow.systems import sinan

# ver todas as doenças disponíveis
sinan.doencas()   # retorna dict {código: descrição}

# baixar e ler
df = sinan.ler(doenca="DENG", ano=2023)   # Dengue
df = sinan.ler(doenca="TUBE", ano=2022)   # Tuberculose
df = sinan.ler(doenca="CHIK", ano=2023)   # Chikungunya

# dados preliminares do ano corrente
df = sinan.ler(doenca="DENG", ano=2024, preliminar=True)

# listar arquivos disponíveis
sinan.listar(doenca="DENG")
sinan.listar(preliminar=True)
```

---

## Cache

Por padrão os arquivos são salvos em `~/.susflow/cache/`, espelhando a estrutura do FTP:

```
~/.susflow/cache/
└── dissemin/publicos/
    ├── SINASC/NOV/DNRES/DNSP2022.dbc
    ├── SIM/CID10/DORES/DOSP2023.dbc
    └── SINAN/DADOS/FINAIS/DENGBR23.dbc
```

Um arquivo já baixado nunca é baixado novamente, a menos que `forcar=True` seja passado.

---

## Escopo

### v1 — implementado

| Sistema | Granularidade | Formato | Status |
|---------|--------------|---------|--------|
| SINASC | anual / por UF | `.dbc` | ✅ |
| SIM (por UF) | anual / por UF | `.dbc` | ✅ |
| SIM (especial) | anual / nacional | `.dbc` | ✅ |
| SINAN | anual / nacional | `.dbc` | ✅ |
| SIHSUS | mensal / por UF | `.dbc` | 🔄 próximo |
| SIASUS | mensal / por UF | `.dbc` | 🔄 próximo |
| CNES | mensal / por UF | `.dbc` | 🔄 próximo |
| PNI | anual / por UF | `.dbf` | 🔄 próximo |

### v1 — features possíveis com os dados já disponíveis

| Feature | Sistemas envolvidos |
|---------|-------------------|
| Taxa de mortalidade infantil por UF/ano | SIM + SINASC + IBGE/POP |
| Série histórica de nascimentos por UF | SINASC |
| Mapa de doenças notificadas por ano | SINAN |
| Evolução de internações hospitalares | SIHSUS |
| Cobertura vacinal por UF | PNI |
| Distribuição de estabelecimentos de saúde | CNES |
| Comparativo de produção ambulatorial | SIASUS |
| Mortalidade por causas externas (nacional) | SIM especial (EXT) |
| Óbitos maternos por ano | SIM especial (MAT) |

### v2 — sistemas especializados (planejado)

| Sistema | O que é | Observação |
|---------|---------|------------|
| CIH / CIHA | Comunicação Hospitalar | CIH encerrou em 2010, CIHA substituiu |
| e-SUS Notifica | Notificações de COVID-19 | Escopo específico da pandemia |
| PCE | Controle de Esquistossomose | Subconjunto do SINAN |
| Painel Oncologia | Registros de câncer | Desde 2013 |
| RESP | Síndrome Congênita do Zika | Surto 2015-2016 |
| SISCOLO / SISMAMA | Cânceres de colo e mama | Dentro do SISCAN |
| SISPRENATAL | Pré-natal | Monitoramento da gestação |

---

## Fontes FTP

Os dados são obtidos via FTP do DATASUS (`ftp.datasus.gov.br`). A estrutura principal fica em `/dissemin/publicos/`:

```
/dissemin/publicos/
├── SIM/
│   ├── CID10/DORES/      ← óbitos por UF (DO{UF}{YYYY}.dbc)
│   ├── CID10/DOFET/      ← óbitos especiais nacionais (DO{TIPO}{YY}.dbc)
│   └── PRELIM/
├── SINASC/
│   └── NOV/DNRES/        ← nascidos vivos (DN{UF}{YYYY}.dbc)
├── SINAN/
│   ├── DADOS/FINAIS/     ← agravos finais ({DOENÇA}BR{YY}.dbc)
│   └── DADOS/PRELIM/     ← agravos preliminares
├── SIHSUS/200801_/Dados/ ← internações ({PREFIX}{UF}{YY}{MM}.dbc)
├── SIASUS/200801_/Dados/ ← ambulatório ({PREFIX}{UF}{YY}{MM}.dbc)
├── CNES/200508_/Dados/   ← estabelecimentos ({TIPO}/{TIPO}{UF}{YY}{MM}.dbc)
└── PNI/DADOS/            ← vacinação (DPNI{UF}{YY}.DBF)
```

### Padrão de arquivos por sistema

| Sistema | Padrão de arquivo | Granularidade | Formato |
|---------|-------------------|---------------|---------|
| SINASC | `DN{UF}{YYYY}.dbc` | anual / por UF | `.dbc` |
| SIM UF | `DO{UF}{YYYY}.dbc` | anual / por UF | `.dbc` |
| SIM especial | `DO{TIPO}{YY}.dbc` | anual / nacional | `.dbc` |
| SINAN | `{DOENÇA}BR{YY}.dbc` | anual / nacional | `.dbc` |
| SIHSUS | `{PREFIX}{UF}{YY}{MM}.dbc` | mensal / por UF | `.dbc` |
| SIASUS | `{PREFIX}{UF}{YY}{MM}.dbc` | mensal / por UF | `.dbc` |
| PNI | `DPNI{UF}{YY}.DBF` | anual / por UF | `.dbf` |

---

## Fluxo dos dados

```
FTP DATASUS (.dbc)
      │
      ▼
Descomprimir blast → .dbf
      │
      ▼
Ler colunas → DataFrame
      │
      ▼
Usuário trabalha com os dados
```

O único passo não trivial é `.dbc → .dbf`, que usa um algoritmo de compressão proprietário chamado **blast** (variante do PKWARE). A lib [`pyreaddbc`](https://github.com/AlertaDengue/PySUS) resolve isso em Python puro.

---

## Ferramentas de mapeamento FTP

O diretório `tools/` contém scripts para explorar e mapear a estrutura do FTP do DATASUS:

```bash
# mapear sistemas da v1 (padrão)
python tools/mapear_ftp.py

# salvar resultado em tools/mapas/
python tools/mapear_ftp.py --salvar --quiet

# explorar caminho específico
python tools/mapear_ftp.py --alvo /dissemin/publicos/SINAN/DADOS

# descer mais um nível de subdiretórios
python tools/mapear_ftp.py --profundo --salvar
```
