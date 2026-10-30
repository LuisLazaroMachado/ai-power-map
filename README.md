# The AI Power Map

Analysis of the geographic, organizational, and technological concentration of **3,405 artificial intelligence models** (1950–2026) from the public [Epoch AI](https://epoch.ai/data) dataset, with a reproducible Python pipeline and data sources for a Tableau dashboard.

**Technologies:** Python (pandas, scikit-learn, matplotlib, seaborn), Jupyter, Tableau

> **Central question:** who holds the technological power in AI today, and what factors explain that concentration?

## Dashboard

![Tableau dashboard overview](docs/images/dashboard_vista_general.png)

The dashboard data sources are in [`outputs/tableau/`](outputs/tableau/): a star schema (`fact_models` + 4 dimensions), the analytical table `fact_models_gold.csv`, the segmentation tables `seg_*.csv`, and the PCA/t-SNE coordinates.

## Key Findings

- **Two blocs account for more than 80% of production:** Anglosphere (58%, 1,991 models) and China (25%, 847 models). Latin America appears with 2 models.
- **Industry displaced academia:** it grew from 270 models in the 2010s to 1,801 in the 2020s (Academia: 349 → 677) and accounts for 62% of the models in the 2020s.
- **A single domain dominates:** Language represents 48% of all models.
- **Technical structure (PCA and t-SNE on 632 models):** models tend to cluster by technological era and producer type, not by geopolitical bloc. The bloc was not an input variable, so this is an indirect reading.

Details and limitations in the [executive summary](docs/resumen_ejecutivo.md).

## Analysis Visualizations

PCA (global structure) versus t-SNE (local structure), colored by technological era:

![PCA vs t-SNE](outputs/reports/pca_vs_tsne.png)

## What Was Analyzed

The notebooks are run in order. Each one lists its inputs and outputs in its header.

| # | Notebook | What it does | Techniques and decisions |
|---|---|---|---|
| 01 | [`perfilado_y_limpieza`](notebooks/01_perfilado_y_limpieza.ipynb) | Profiles the raw dataset (3,509 rows × 57 columns) and cleans it down to 3,405 × 22 | Null and cardinality analysis, deduplication by `Model`, category harmonization, imputation with `Unknown` for categorical variables |
| 02 | [`analisis_exploratorio`](notebooks/02_analisis_exploratorio.ipynb) | Explores the distribution by year, country, domain, organization, and accessibility | Distributions, evolution by decade, correlation between numeric variables |
| 03 | [`modelo_de_datos_plano_vs_estrella`](notebooks/03_modelo_de_datos_plano_vs_estrella.ipynb) | Compares two data structures for Tableau and picks one | Structural validation metrics; star schema versus flat table |
| 04 | [`segmentacion_y_metricas`](notebooks/04_segmentacion_y_metricas.ipynb) | Segments the data and computes derived metrics (Gold layer) | Geopolitical bloc, technological era, access type, log(x+1), percentage share, cumulative totals |
| 05 | [`reduccion_dimensionalidad_pca_tsne`](notebooks/05_reduccion_dimensionalidad_pca_tsne.ipynb) | Looks for technical structure in 632 models | StandardScaler, PCA (variance and loadings), t-SNE, validation with a different seed |
| — | [`exploraciones/`](notebooks/exploraciones/exploracion_preprocesamiento_pca_kmeans.ipynb) | Preprocessing for PCA + K-Means (1,212 rows) | Feature selection by coverage and one-hot encoding. K-Means was never run; not part of the final analysis |

### Decisions and Options Evaluated

| Decision | Options | Chosen | Why |
|---|---|---|---|
| Data model for Tableau | Flat table, star schema (snowflake was discarded as unnecessary) | Star schema | Keeps all 3,405 rows, produces no null keys, and avoids repeating attributes. The flat table is kept as a fallback |
| Numeric nulls | Impute or keep | Keep | Imputing would bias highly skewed variables |
| Categorical nulls | Drop rows or label | Label as `Unknown` | No rows are lost in the analysis |
| Scaling before PCA | StandardScaler or MinMaxScaler | StandardScaler | MinMaxScaler is more sensitive to extreme outliers |
| Numeric variables | Original or log(x+1) | log(x+1) | Reduces skewness and avoids log(0) |
| Dimensionality reduction | PCA, t-SNE, or both | Both | PCA shows global structure; t-SNE shows local neighborhoods |
| Clustering with K-Means | Evaluate with silhouette (k from 2 to 8) | Not used | Silhouette between 0.21 and 0.33 and very uneven clusters (up to 86.6% in one): no clearly separated groups |

### Concepts Used

| Concept | In plain words |
|---|---|
| **PCA** | Summarizes many variables into a few dimensions while preserving as much variance as possible. Useful for seeing which variables explain the most |
| **t-SNE** | Places similar items close together. It preserves local neighborhoods, not global distances, and should not be read as the real distance between groups |
| **StandardScaler** | Centers each variable at mean 0 and standard deviation 1, so that none dominates because of large values |
| **One-hot encoding** | Converts each category into a 0/1 column |
| **Star schema** | A fact table connected to dimension tables |
| **Medallion architecture** | Bronze (raw data) → Silver (clean data) → Gold (analysis-ready data) |

## Data Architecture

| Layer | Location | Contents |
|---|---|---|
| Bronze | `data/raw/all_ai_models.csv` | Original dataset (3,509 × 57) |
| Silver | `data/processed/all_ai_models_clean.csv` | Clean dataset (3,405 × 22) |
| Gold | `outputs/tableau/` | Star schema, `fact_models_gold.csv` (3,405 × 45), `seg_*` tables, and PCA/t-SNE embedding (632 rows) |

## How to Reproduce

Requires Python 3.10 or higher.

```bash
git clone https://github.com/LuisLazaroMachado/ai-power-map
cd ai-power-map

python -m venv .venv
.venv\Scripts\activate        # Windows (PowerShell). On Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt

python -m src.pipeline         # regenerates Silver and Gold (cleaning, star schema, segmentation)
jupyter lab                    # open notebooks/ and run them in order
```

`python -m src.pipeline` regenerates all tables in `data/processed/` and `outputs/` except the PCA/t-SNE analysis, which is generated by running notebook 05.

## Repository Structure

```text
ai-power-map/
├── LICENSE
├── requirements.txt
├── data/
│   ├── README.md             # data source, license, and modifications
│   ├── raw/                  # Bronze: all_ai_models.csv (Epoch AI)
│   └── processed/            # Silver: all_ai_models_clean.csv
├── notebooks/
│   ├── 01_perfilado_y_limpieza.ipynb
│   ├── 02_analisis_exploratorio.ipynb
│   ├── 03_modelo_de_datos_plano_vs_estrella.ipynb
│   ├── 04_segmentacion_y_metricas.ipynb
│   ├── 05_reduccion_dimensionalidad_pca_tsne.ipynb
│   └── exploraciones/
├── src/
│   ├── config.py             # paths and column lists
│   ├── io_utils.py           # CSV reading and writing
│   ├── preprocessing.py      # Bronze → Silver
│   ├── modeling.py           # flat table and star schema
│   ├── analytics.py          # segmentation and metrics (Gold)
│   └── pipeline.py           # python -m src.pipeline
├── outputs/
│   ├── reports/              # quality metrics and PCA/t-SNE figures
│   └── tableau/              # dashboard data sources
└── docs/
    ├── resumen_ejecutivo.md
    ├── modelo_de_datos_y_preprocesamiento.md
    └── images/               # dashboard screenshots
```

## Limitations

- PCA and t-SNE cover 632 of 3,405 models (18.6%): only those with complete key numeric variables.
- `Parameters`, `Training compute (FLOP)`, and `Citations` have 34%, 60%, and 57% nulls. They were not imputed.
- The geopolitical blocs explicitly map 28 countries. The 81 models (2.4%) from 20 other countries fall into the "Otro" (Other) bloc.

## Licenses, Data Source, and Authors

- **Code:** [MIT](LICENSE) license.
- **Data:** Epoch AI, *All AI Models*, under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Derived data (`data/processed/` and `outputs/`) retains attribution to Epoch AI. Details, citation, and list of modifications in [`data/README.md`](data/README.md).
- **Authors:** Fabian Marcelo Rojas Cuadros and Lazaro Machado Luis Isaac. Team DataChasquiAILab, Data Visualization course, Universidad Peruana de Ciencias Aplicadas.
