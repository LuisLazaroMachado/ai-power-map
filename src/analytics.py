"""
analytics.py
Segmentación, métricas derivadas y tablas resumen (capa Gold) para Tableau.
"""
from __future__ import annotations
import pandas as pd
import numpy as np


# ── 1. SEGMENTACIÓN ──────────────────────────────────────────────────────────

BLOQUES_GEOPOLITICOS = {
    "United States of America": "Anglosphere",
    "United Kingdom of Great Britain and Northern Ireland": "Anglosphere",
    "Canada": "Anglosphere",
    "Australia": "Anglosphere",
    "China": "China",
    "Hong Kong": "China",
    "Germany": "Europa",
    "France": "Europa",
    "Switzerland": "Europa",
    "Italy": "Europa",
    "Netherlands": "Europa",
    "Spain": "Europa",
    "Sweden": "Europa",
    "Denmark": "Europa",
    "Belgium": "Europa",
    "Korea (Republic of)": "Asia-Pacífico",
    "Japan": "Asia-Pacífico",
    "Singapore": "Asia-Pacífico",
    "India": "Asia-Pacífico",
    "Israel": "Medio Oriente",
    "United Arab Emirates": "Medio Oriente",
    "Saudi Arabia": "Medio Oriente",
    "Russia": "Rusia",
    "Brazil": "Latinoamérica",
    "Mexico": "Latinoamérica",
    "Argentina": "Latinoamérica",
    "Chile": "Latinoamérica",
    "Peru": "Latinoamérica",
}

ERAS_TECNOLOGICAS = [
    (1950, 1979, "Era Simbólica (1950-1979)"),
    (1980, 1999, "Era Conexionista (1980-1999)"),
    (2000, 2011, "Era Deep Learning (2000-2011)"),
    (2012, 2016, "Era GPU (2012-2016)"),
    (2017, 2022, "Era Transformer (2017-2022)"),
    (2023, 2026, "Era LLM (2023-2026)"),
]


def add_bloque_geopolitico(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega columna bloque_geopolitico basada en país de organización."""
    out = df.copy()
    out["bloque_geopolitico"] = (
        out["Country (of organization)"]
        .map(BLOQUES_GEOPOLITICOS)
        .fillna("Otro")
    )
    return out


def add_era_tecnologica(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega columna era_tecnologica basada en el año de publicación."""
    out = df.copy()

    def asignar_era(year):
        if pd.isna(year):
            return "Desconocido"
        for inicio, fin, nombre in ERAS_TECNOLOGICAS:
            if inicio <= int(year) <= fin:
                return nombre
        return "Desconocido"

    out["era_tecnologica"] = out["Year"].apply(asignar_era)
    return out


def add_tipo_acceso(df: pd.DataFrame) -> pd.DataFrame:
    """Simplifica Model accessibility en 3 categorías: Abierto, Cerrado, Unknown."""
    out = df.copy()

    def clasificar(val):
        if pd.isna(val) or val == "Unknown":
            return "Unknown"
        if "Open" in str(val):
            return "Abierto"
        return "Cerrado"

    out["tipo_acceso"] = out["Model accessibility"].apply(clasificar)
    return out


# ── 2. MÉTRICAS DERIVADAS ────────────────────────────────────────────────────

def add_log_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega versiones logarítmicas de variables numéricas sesgadas.
    log(x+1) evita log(0) para valores en cero.
    Útil para visualización en Tableau donde la escala lineal aplana los datos.
    """
    out = df.copy()
    cols = ["Parameters", "Training compute (FLOP)", "Citations"]
    for col in cols:
        if col in out.columns:
            nombre = col.lower().replace(" ", "_").replace("(", "").replace(")", "")
            out[f"log_{nombre}"] = np.log1p(out[col])
    return out


def add_modelos_acumulados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula el acumulado de modelos por año a nivel global y por país.
    Permite vista longitudinal de crecimiento en Tableau.
    """
    out = df.copy()

    # Acumulado global por año
    anual = (
        out.groupby("Year")
        .size()
        .reset_index(name="modelos_anio")
        .sort_values("Year")
    )
    anual["modelos_acumulados_global"] = anual["modelos_anio"].cumsum()
    out = out.merge(anual[["Year", "modelos_anio", "modelos_acumulados_global"]],
                    on="Year", how="left")
    return out


def add_participacion_pais(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula participación porcentual de cada país sobre el total de modelos.
    Denominador: total de modelos en el dataset.
    """
    out = df.copy()
    total = len(out)
    participacion = (
        out.groupby("Country (of organization)")
        .size()
        .reset_index(name="modelos_pais")
    )
    participacion["pct_participacion_pais"] = (
        participacion["modelos_pais"] / total * 100
    ).round(2)
    out = out.merge(participacion, on="Country (of organization)", how="left")
    return out


def add_participacion_dominio(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula participación porcentual de cada dominio sobre el total de modelos.
    """
    out = df.copy()
    total = len(out)
    participacion = (
        out.groupby("Domain")
        .size()
        .reset_index(name="modelos_dominio")
    )
    participacion["pct_participacion_dominio"] = (
        participacion["modelos_dominio"] / total * 100
    ).round(2)
    out = out.merge(participacion, on="Domain", how="left")
    return out


# ── 3. VARIABLES BINARIAS (para PCA/t-SNE) ───────────────────────────────────

def add_dummy_variables(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea variables binarias desde categóricas para enriquecer
    el análisis y preparar el componente avanzado PCA/t-SNE.
    Técnica: One-Hot Encoding parcial sobre categorías principales.
    """
    out = df.copy()

    # Desde Domain
    dominios_principales = [
        "Language", "Vision", "Biology",
        "Multimodal", "Image generation", "Speech"
    ]
    for dominio in dominios_principales:
        out[f"es_{dominio.lower().replace(' ', '_')}"] = (
            out["Domain"] == dominio
        ).astype(int)

    # Desde Organization categorization
    out["es_industry"] = (
        out["Organization categorization"] == "Industry"
    ).astype(int)
    out["es_academia"] = (
        out["Organization categorization"] == "Academia"
    ).astype(int)

    # Desde Model accessibility
    out["es_abierto"] = (
        out["tipo_acceso"] == "Abierto"
    ).astype(int)

    # Desde Year
    out["es_post_2020"] = (out["Year"] >= 2020).astype(int)
    out["es_post_2017"] = (out["Year"] >= 2017).astype(int)

    return out


# ── 4. PIPELINE COMPLETO ─────────────────────────────────────────────────────

def build_analytical_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica todas las transformaciones analíticas en secuencia.
    Retorna el dataset Gold listo para Tableau y para el análisis PCA/t-SNE.
    """
    out = df.copy()
    out = add_bloque_geopolitico(out)
    out = add_era_tecnologica(out)
    out = add_tipo_acceso(out)
    out = add_dummy_variables(out)
    out = add_log_metrics(out)
    out = add_modelos_acumulados(out)
    out = add_participacion_pais(out)
    out = add_participacion_dominio(out)
    return out


def build_segment_summaries(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """
    Genera tablas resumen por segmento para Tableau.
    Retorna un diccionario con todas las tablas analíticas.
    """
    # Resumen por país y año
    pais_anio = (
        df.groupby(["Country (of organization)", "bloque_geopolitico", "Year"])
        .size()
        .reset_index(name="modelos")
    )

    # Resumen por bloque geopolítico y era
    bloque_era = (
        df.groupby(["bloque_geopolitico", "era_tecnologica"])
        .size()
        .reset_index(name="modelos")
    )

    # Resumen por dominio y era
    dominio_era = (
        df.groupby(["Domain", "era_tecnologica"])
        .size()
        .reset_index(name="modelos")
    )

    # Resumen por tipo de organización y era
    org_era = (
        df.groupby(["Organization categorization", "era_tecnologica"])
        .size()
        .reset_index(name="modelos")
    )

    # Resumen por acceso y era
    acceso_era = (
        df.groupby(["tipo_acceso", "era_tecnologica"])
        .size()
        .reset_index(name="modelos")
    )

    return {
        "seg_pais_anio": pais_anio,
        "seg_bloque_era": bloque_era,
        "seg_dominio_era": dominio_era,
        "seg_org_era": org_era,
        "seg_acceso_era": acceso_era,
    }
