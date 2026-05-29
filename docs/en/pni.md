 # PNI — National Immunization Program

 FTP base: `/dissemin/publicos/PNI/DADOS/`

 ---

 ## Available data types

 | Type   | Function               | Returns     | Description                                      |
 | ------ | ---------------------- | ----------- | ----------------------------------------------- |
 | By state | `read(uf, year)`     | `DataFrame` | Immunization records for a state and year       |
 | By state | `download(uf, year)` | `Path`      | Raw `.DBF` file for the state                   |

 ---

 ## Data by state and year — `DADOS/`

 **File pattern:** `DPNI{UF}{YY}.DBF` (year suffix uses 2 digits)

 **Coverage:** 1994–2019, all 27 states

 **Granularity:** annual / by state

 ```python
 from susflow.systems import pni

 # Download (if needed) and load the data into a DataFrame
 df = pni.read(uf="SP", year=2015)

 # Download only the raw file
 path = pni.download(uf="RJ", year=2010)

 # List files filtered by a specific state
 files = pni.list_files(uf="PB")
 ```

 ### Main DataFrame variables

 > **Variability note:** Because coverage spans a long period (1994–2019), column structures in the `.DBF` files may vary depending on the year and system updates. Below are the most common base variables found across vaccine coverage series and dose counts:

 | Variable               | Type        | Description                                                             |
 | ---------------------- | ----------- | ----------------------------------------------------------------------- |
 | `CODMUNRES` / `MUNCOD` | str         | IBGE municipality code (usually 6 digits)                               |
 | `CODVAC` / `VACCOD`    | str         | Vaccine code (e.g. BCG, Polio, MMR)                                      |
 | `DOSE`                 | str         | Dose type/number (1st dose, 2nd dose, booster, single dose)             |
 | `FXETARIA` / `FAIXA`   | str         | Age-group identifier code                                                |
 | `QTDE` / `NUM_DOSES`   | int / float | Number of doses recorded                                                 |
 | `COBER` / `COBERTURA`  | float       | Vaccination coverage rate for the region (when available)               |
 | `POPULACAO`            | int / float | Estimated target population used to calculate coverage                  |

 ---

 ## Recommended workflow

 ```
 1. Explore what is available on the FTP
    pni.list_files(uf="PB")                       ← lists all years for Paraíba

 2. Download and process the data
    df = pni.read(uf="SP", year=2015)             ← immunization data for SP in 2015

 3. Persist locally in an optimized format
    df.to_parquet("pni_sp_2015.parquet", index=False)
 ```

 ---

 ## Notes

 - **File format:** Unlike some DATASUS systems (e.g. SINASC), PNI files in this folder are plain **.DBF** (no proprietary _blast_ compression). They are read directly by the library using the internal `dbfread` implementation in `reader.py`.
 - **Year suffix rule:** Files use a 2-digit year suffix (`YY`). Years 1994–1999 use `94`–`99`, while 2000–2009 use `00`–`09`. The library normalizes transparently using `year % 100`.
 - **Series limits:** This FTP directory ends in **2019**. There are no later years mapped in this module (`year_range: 1994–2019`). Passing years outside this scope will raise a `ValueError`.
 - **Municipality codes:** As with SINASC, municipalities are identified by IBGE codes. To join with municipality names or health regionalizations, correlate with auxiliary tables (e.g. `CADMUN`).
