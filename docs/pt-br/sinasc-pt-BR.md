 # SINASC — Sistema de Informações sobre Nascidos Vivos

 Base FTP: `ftp.datasus.gov.br/dissemin/publicos/SINASC/NOV/`

 ---

 ## Tipos de dados disponíveis

 | Tipo | Função | Retorno | Descrição |
 |------|--------|---------|-----------|
 | Por UF | `ler(uf, ano)` | `DataFrame` | Nascidos vivos registrados em uma UF, por ano |
 | Por UF | `baixar(uf, ano)` | `Path` | Arquivo `.dbc` bruto da UF |
 | Nacional | `ler_nacional(ano)` | `DataFrame` | Agregado nacional (série incompleta: 2014–2017) |
 | Nacional | `baixar_nacional(ano)` | `Path` | Arquivo `.dbc` do agregado nacional |
 | Exceções | `ler_excecao(ano)` | `DataFrame` | Registros suplementares pontuais |
 | Exceções | `baixar_excecao(ano)` | `Path` | Arquivo `.dbc` de exceção |
 | Documentação | `baixar_docs(arquivo?)` | `Path / list[Path]` | Layouts, estrutura e legislação |

 ---

 ## Dados por UF — `DNRES/`

 **Padrão de arquivo:** `DN{UF}{YYYY}.dbc`  
 **Cobertura:** 1996–2022, todas as 27 UFs  
 **Granularidade:** anual / por UF

 ```python
 from susflow.systems import sinasc

 df = sinasc.ler(uf="SP", ano=2022)
 path = sinasc.baixar(uf="RJ", ano=2021)
 arquivos = sinasc.listar(uf="MG")
 ```

 ### Principais variáveis do DataFrame

 | Variável | Tipo | Descrição |
 |----------|------|-----------|
 | `DTNASC` | str | Data do nascimento (DDMMAAAA) |
 | `SEXO` | str | Sexo (1=Masc, 2=Fem, 0=Ignorado) |
 | `PESO` | str | Peso ao nascer (gramas) |
 | `GESTACAO` | str | Semanas de gestação (codificado) |
 | `GRAVIDEZ` | str | Tipo de gravidez (1=Única, 2=Dupla, 3=Tripla+) |
 | `PARTO` | str | Tipo de parto (1=Vaginal, 2=Cesáreo) |
 | `CONSULTAS` | str | Número de consultas pré-natal |
 | `APGAR1` | str | Índice de Apgar no 1º minuto |
 | `APGAR5` | str | Índice de Apgar no 5º minuto |
 | `RACACOR` | str | Raça/cor do recém-nascido |
 | `IDADEMAE` | str | Idade da mãe |
 | `ESTCIVMAE` | str | Estado civil da mãe |
 | `ESCMAE` | str | Escolaridade da mãe |
 | `CODMUNRES` | str | Código IBGE do município de residência da mãe |
 | `CODMUNNASC` | str | Código IBGE do município de nascimento |
 | `CODESTAB` | str | Código do estabelecimento de saúde |
 | `LOCNASC` | str | Local do nascimento (hospital, domicílio, etc.) |
 | `IDANOMAL` | str | Anomalia congênita identificada |
 | `KOTELCHUCK` | str | Índice de Kotelchuck (adequação do pré-natal) |

 > Para a lista completa de variáveis e seus códigos, baixe a documentação técnica com `sinasc.baixar_docs()`.

 ---

 ## Agregado nacional — `DNBR`

 **Padrão de arquivo:** `DNBR{YYYY}.dbc`  
 **Cobertura:** 2014–2017 (série incompleta — apenas esses anos foram confirmados no FTP)  
 **Granularidade:** anual / nacional

 ```python
 df = sinasc.ler_nacional(ano=2015)
 path = sinasc.baixar_nacional(ano=2016)
 arquivos = sinasc.listar_nacional()
 ```

 > Para análises nacionais fora desse intervalo, consolide os dados por UF manualmente.

 ---

 ## Arquivos de exceção — `DNEX`

 **Padrão de arquivo:** `DNEX{YYYY}.dbc`  
 **Natureza:** arquivos pontuais com registros suplementares — não é uma série regular  
 **Confirmado no FTP:** `DNEX2021.dbc` (único arquivo identificado)

 ```python
 df = sinasc.ler_excecao(ano=2021)
 path = sinasc.baixar_excecao(ano=2021)
 arquivos = sinasc.listar_excecoes()
 ```

 ---

 ## Documentação técnica — `DOCS/`

 > **Atenção:** o caminho FTP deste diretório ainda não foi confirmado por mapeamento direto. Se o download falhar, rode `python tools/mapear_ftp.py --alvo /dissemin/publicos/SINASC/NOV` para localizar o diretório correto.

 | Arquivo | Descrição | Quando usar |
 |---------|-----------|-------------|
 | `Estrutura_SINASC_para_CD.pdf` | Estrutura dos arquivos (formato legado de CD-ROM) | Bases antigas distribuídas em CD |
 | `Legislacao_PDF.pdf` | Legislação relacionada ao SINASC | Referência normativa |
 | `NASC98.HLP` | Arquivo de ajuda do sistema legado (1998) | Bases de 1996–1998 |
 | `Portaria.pdf` | Portaria regulamentadora | Referência normativa |

 ```python
 # ver o que está disponível
 print(sinasc.listar_docs())

 # baixar um documento específico
 path = sinasc.baixar_docs("Estrutura_SINASC_para_CD.pdf")
 path = sinasc.baixar_docs("NASC98.HLP")  # para bases de 1996–1998

 # baixar todos de uma vez
 paths = sinasc.baixar_docs()

 # salvar em pasta específica
 path = sinasc.baixar_docs("Legislacao_PDF.pdf", destino="/meus/dados/sinasc")
 ```

 ---

 ## Fluxo recomendado

 ```
 1. Explorar o que existe
    sinasc.listar(uf="SP")
    sinasc.listar_nacional()
    sinasc.listar_excecoes()

 2. Baixar os dados
    df = sinasc.ler(uf="SP", ano=2022)           ← microdados por UF
    df = sinasc.ler_nacional(ano=2015)            ← agregado nacional
    df = sinasc.ler_excecao(ano=2021)             ← registros suplementares

 3. Baixar referências para entender os campos
    sinasc.baixar_docs("Estrutura_SINASC_para_CD.pdf")
    sinasc.baixar_docs("NASC98.HLP")              ← para bases de 1996–1998
 ```

 ---

 ## Notas

 - Arquivos `.dbc` são DBF comprimidos com o algoritmo proprietário **blast** (PKWARE). A biblioteca descomprime automaticamente via `pyreaddbc`.
 - O campo `GESTACAO` usa codificação própria: 1=menos de 22 semanas, 2=22–27, 3=28–31, 4=32–36, 5=37–41, 6=42+, 9=ignorado.
 - O campo `PESO` está em gramas. Valores como `9999` indicam ignorado.
 - Municípios são identificados pelo código IBGE de 6 dígitos. Use `CADMUN.DBF` do SIM para cruzar com nomes.
 - O índice de Kotelchuck (`KOTELCHUCK`) classifica a adequação do pré-natal combinando número de consultas e início do acompanhamento.
 - Para bases anteriores a 1999, a estrutura dos campos pode diferir — consulte `NASC98.HLP` e `Estrutura_SINASC_para_CD.pdf`.
 - O agregado nacional `DNBR` só existe para 2014–2017. Para outros anos, some os dados por UF.
