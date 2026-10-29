"""
Pipeline reproducible: datos crudos (Bronze) -> dataset limpio (Silver) -> tablas analíticas (Gold).

Uso, desde la raíz del proyecto:
    python -m src.pipeline

El análisis PCA/t-SNE (notebook 05) se ejecuta aparte porque es un análisis, no una transformación de datos.
"""
from __future__ import annotations

from .analytics import build_analytical_dataset, build_segment_summaries
from .config import CLEAN_DATASET, OUTPUTS_REPORTS, OUTPUTS_TABLEAU, RAW_DATASET
from .io_utils import load_csv, save_csv
from .modeling import build_flat_model, build_star_schema, compare_model_options
from .preprocessing import build_quality_summary, clean_ai_models


def main() -> None:
    # Bronze -> Silver
    raw_df = load_csv(RAW_DATASET)
    clean_df = clean_ai_models(raw_df)
    save_csv(clean_df, CLEAN_DATASET)
    save_csv(build_quality_summary(raw_df, clean_df), OUTPUTS_REPORTS / "quality_summary.csv")

    # Modelo de datos para Tableau: tabla plana vs. esquema estrella
    save_csv(compare_model_options(clean_df), OUTPUTS_REPORTS / "model_options_comparison.csv")
    for name, table in {**build_flat_model(clean_df), **build_star_schema(clean_df)}.items():
        save_csv(table, OUTPUTS_TABLEAU / f"{name}.csv")

    # Silver -> Gold: segmentación, métricas derivadas y tablas resumen
    gold_df = build_analytical_dataset(clean_df)
    save_csv(gold_df, OUTPUTS_TABLEAU / "fact_models_gold.csv")
    for name, table in build_segment_summaries(gold_df).items():
        save_csv(table, OUTPUTS_TABLEAU / f"{name}.csv")

    print("Pipeline ejecutado correctamente.")
    print(f"Silver: {CLEAN_DATASET} ({len(clean_df):,} filas)")
    print(f"Gold:   {OUTPUTS_TABLEAU} ({gold_df.shape[1]} columnas en fact_models_gold.csv)")
    print(f"Reportes: {OUTPUTS_REPORTS}")


if __name__ == "__main__":
    main()
