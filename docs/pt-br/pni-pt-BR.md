 # PNI — Programa Nacional de Imunizações

 Base FTP: `/dissemin/publicos/PNI/DADOS/`

 ---

 ## Tipos de dados disponíveis

 | Tipo   | Função            | Retorno     | Descrição                                      |
 | ------ | ----------------- | ----------- | ---------------------------------------------- |
 | Por UF | `read(uf, year)`    | `DataFrame` | Dados de imunização registrados na UF, por ano |
 | Por UF | `download(uf, year)` | `Path`      | Arquivo `.DBF` bruto da UF                     |

 ---

 ## Dados por UF e Ano — `DADOS/`

 **Padrão de arquivo:** `DPNI{UF}{YY}.DBF` (Sufixo do ano com 2 dígitos)

 **Cobertura:** 1994–2019, todas as 27 UFs

 **Granularidade:** anual / por UF

 ```python
 from susflow.systems import pni

 # Baixa (se necessário) e carrega os dados em um DataFrame
 df = pni.read(uf="SP", year=2015)

 # Apenas realiza o download do arquivo bruto
 path = pni.download(uf="RJ", year=2010)

 # Lista os arquivos filtrando por uma UF específica
 arquivos = pni.list_files(uf="PB")

 ```

 ### Principais variáveis do DataFrame

 > **Nota de Variabilidade:** Como a cobertura do PNI é extensa (1994–2019), a estrutura de colunas dos arquivos `.DBF` pode variar significativamente dependendo do período e das atualizações do sistema de informação do Ministério da Saúde. Abaixo estão listadas as variáveis base mais comuns encontradas nas séries históricas de coberturas vacinais e doses aplicadas:

 | Variável               | Tipo        | Descrição                                                             |
 | ---------------------- | ----------- | --------------------------------------------------------------------- |
 | `CODMUNRES` / `MUNCOD` | str         | Código IBGE do município (geralmente 6 dígitos)                       |
 | `CODVAC` / `VACCOD`    | str         | Código da vacina (ex: BCG, Poliomielite, Tríplice Viral)              |
 | `DOSE`                 | str         | Tipo/Número da dose (1ª dose, 2ª dose, reforço, dose única)           |
 | `FXETARIA` / `FAIXA`   | str         | Código identificador da faixa etária do vacinado                      |
 | `QTDE` / `NUM_DOSES`   | int / float | Quantidade de doses aplicadas registradas                             |
 | `COBER` / `COBERTURA`  | float       | Taxa de cobertura vacinal calculada para a região (quando disponível) |
 | `POPULACAO`            | int / float | População alvo estimada para o cálculo da cobertura                   |

 ---

 ## Fluxo recomendado

 ```
 1. Explorar o que existe no FTP
    pni.list_files(uf="PB")                           ← lista todos os anos da Paraíba

 2. Baixar e processar os dados
    df = pni.read(uf="SP", year=2015)               ← dados de imunização de SP em 2015

 3. Persistir localmente de forma otimizada
    # Recomendado converter para Parquet após a leitura para melhorar a performance
    df.to_parquet("pni_sp_2015.parquet", index=False)

 ```

 ---

 ## Notas

 - **Formato dos Arquivos:** Diferente de outros sistemas do DATASUS (como o SINASC), os arquivos do PNI nesta pasta estão em formato **.DBF puro** (sem compressão proprietária _blast_). Eles são lidos diretamente pela biblioteca utilizando o `dbfread` interno do módulo `reader.py`.
 - **Regra de Sufixo do Ano:** O arquivo utiliza o ano com 2 dígitos (`YY`). Anos de 1994 a 1999 usam `94` a `99`, enquanto anos de 2000 a 2009 utilizam `00` a `09`. A normalização é feita de forma transparente pela biblioteca utilizando o operador `ano % 100`.
 - **Limites da Série Histórica:** A cobertura de dados deste diretório FTP encerra-se estritamente em **2019**. Não existem dados preliminares ou anos posteriores a este período mapeados neste módulo (`year_range: 1994–2019`). Tentativas de passar anos fora deste escopo resultarão em um `ValueError`.
 - **Códigos de Municípios:** Assim como no SINASC, os municípios são identificados por seus códigos IBGE. Caso precise realizar o cruzamento com o nome das localidades ou regionalizações de saúde, recomenda-se correlacionar com as tabelas auxiliares (`CADMUN`).
