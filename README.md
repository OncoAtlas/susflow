# susflow

Biblioteca Python para acesso e download dos dados abertos do DATASUS. O objetivo é abstrair a complexidade do protocolo FTP, descompressão dos arquivos `.dbc` e leitura dos dados, entregando ao usuário um DataFrame pronto para análise.

---

## Escopo

### v1 — sistemas consolidados (atual)

| Sistema | O que é |
|---------|---------|
| SIM | Sistema de Informações de Mortalidade |
| SINASC | Sistema de Informação de Nascidos Vivos |
| SINAN | Sistema de Informação de Agravos de Notificação |
| SIHSUS | Sistema de Informações Hospitalares do SUS |
| SIASUS | Sistema de Informações Ambulatoriais do SUS |
| CNES | Cadastro Nacional de Estabelecimentos de Saúde |
| PNI | Programa Nacional de Imunizações |

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

```txt
/dissemin/publicos/
├── SIM/
│   ├── CID10/            ← mortalidade a partir de 1996 (CID-10)
│   ├── CID9/             ← mortalidade antes de 1996 (histórico)
│   └── PRELIM/           ← dados preliminares do ano corrente
├── SINASC/
│   ├── NOV/              ← natalidade (dados novos/atuais)
│   ├── 1996_/            ← dados a partir de 1996
│   └── PRELIM/           ← dados preliminares
├── SINAN/
│   ├── DADOS/            ← doenças e agravos
│   └── AUXILIAR/
├── SIHSUS/
│   ├── 200801_/          ← internações a partir de 2008
│   └── 199201_200712/    ← internações 1992-2007 (histórico)
├── SIASUS/
│   ├── 200801_/          ← ambulatório a partir de 2008
│   └── APAC/             ← procedimentos de alta complexidade
├── CNES/
│   └── 200508_/          ← estabelecimentos a partir de 2005
├── PNI/
│   └── DADOS/            ← vacinação
└── IBGE/
    └── POP/              ← populações (para calcular taxas)

/cnes/                    ← pasta separada, ZIPs com base completa mensal
    BASE_DE_DADOS_CNES_YYYYMM.ZIP
```

### Padrão de arquivos por sistema

| Sistema | Caminho FTP | Padrão de arquivo | Granularidade | Formato |
|---------|-------------|-------------------|---------------|---------|
| SINASC | `.../SINASC/NOV/DNRES/` | `DN{UF}{YYYY}.dbc` | anual / por UF | `.dbc` |
| SINAN | `.../SINAN/DADOS/FINAIS/{DOENÇA}/` | `{DOENÇA}BR{YY}.dbc` | anual / nacional | `.dbc` |
| SIHSUS | `.../SIHSUS/200801_/Dados/` | `{PREFIX}{UF}{YY}{MM}.dbc` | mensal / por UF | `.dbc` |
| SIASUS | `.../SIASUS/200801_/Dados/` | `{PREFIX}{UF}{YY}{MM}.dbc` | mensal / por UF | `.dbc` |
| PNI | `.../PNI/DADOS/` | `DPNI{UF}{YY}.DBF` | anual / por UF | `.dbf` |
| IBGE/POP | `.../IBGE/POP/` | `POPBR{YY}.zip` | anual / nacional | `.zip` |

---

## Fluxo dos dados

```txt
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
