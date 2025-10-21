# Gender-Based Violence in Equal Times (GBV_EQ_DB)

GBV_EQ_DB centralises indicators about gender-based violence in Spain and brings together
socioeconomic, political, and cultural datasets that help explain its prevalence. The repository
contains the ETL code that standardises heterogeneous data sources, the SQL schema for the target
PostgreSQL database, and the automation needed to keep the database up to date.

> **Data access:** The raw and cleaned datasets are stored in a private companion repository and are
> therefore not included here. Contact the maintainers to request access if you need to reproduce the
> full pipeline end to end.

## 📂 Repository layout

| Path | Description |
| --- | --- |
| `pipelines/` | Orchestration scripts for dropping/creating schemas, extracting & transforming data, and loading the final tables. |
| `downloaders/` | Source-specific scrapers and API downloaders used during the extract stage (many rely on Selenium). |
| `sql/` | SQL files that define the PostgreSQL schemas, tables, constraints, and helper functions used by the project. |
| `utils/` | Shared helpers for logging, normalisation dictionaries, and script execution. |
| `docs/` | MkDocs project powering the public documentation site, including table-level metadata. |
| `tests/` | Pytest suite covering selected utilities (e.g. normalisation helpers). |

## 🔄 Pipeline overview

1. **Extraction** – The scripts under `downloaders/` pull data from ministerial portals, statistical
   offices, and surveys. Outputs are saved as raw files in the private data repository.
2. **Transformation** – Modules inside `pipelines/extract_transform/` harmonise the raw files into a
   clean tabular format (CSV) following common naming conventions and coding schemes.
3. **Load** – `pipelines/load_data.py` ingests the cleaned CSV files into PostgreSQL. Custom loader
   hooks are available for tables that need post-processing (e.g. EIGE indicators or demographic
   breakdowns).

`pipelines/main.py` ties these stages together. It exposes a CLI that lets you run the full pipeline or
individual steps:

```bash
python pipelines/main.py               # drop → create → extract/transform → load
python pipelines/main.py et --only      # run only the extract/transform stage
python pipelines/main.py load --schema violencia_genero
```

## 💻 Local setup

### Requirements

- Python 3.12+
- PostgreSQL instance accessible from your machine
- (Optional) Google Chrome/Chromedriver for Selenium-based downloaders

### Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Configure environment variables

Pipeline scripts expect a `.env` file at the repository root (or exported shell variables) with the
PostgreSQL credentials:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=gbv_eq
DB_USER=postgres
DB_PASSWORD=secret
```

Additional variables may be required by specific downloaders (e.g. credentials to restricted portals);
consult the script headers inside `downloaders/` for details.

### Prepare the data directory

The pipeline reads from `data/raw/` and `data/clean/` directories, which should mirror the structure
of the private data repository. Ensure these folders are populated before running `extract_transform`
or `load` steps. If you do not have access to the private data repository, request access by contacting the maintainers: leire.rincon@uab.cat or nachodoradollamas@gmail.com.

## ✅ Testing and quality checks

```bash
pytest                      # run unit tests in tests/
ruff check                  # lint the codebase
```

## 📚 Documentation site

The MkDocs configuration (`mkdocs.yml`) builds a bilingual documentation portal.

- Preview locally:
```bash
mkdocs serve
```

- Deployed site: https://nachodll.github.io/GBV_EQ_DB/ — contains the public docs and table-level metadata.

## 📬 Getting help

For questions or issues, open a GitHub issue in this repository or contact the maintainers listed below.

If you have questions about the pipeline or need access to the datasets, reach out to the maintainers:

- Leire Rincón — leire.rincon@uab.cat
- Ignacio Dorado — nachodoradollamas@gmail.com
