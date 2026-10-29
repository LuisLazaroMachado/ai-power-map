# Modelo de datos y preprocesamiento

## Proyecto

**The AI Power Map** analiza la evolución y concentración de modelos de inteligencia artificial registrados en el dataset público de Epoch AI.

## Alcance

Este documento describe el pipeline reproducible que prepara el dataset, compara dos estructuras de modelo de datos y selecciona la fuente recomendada para Tableau. Se ejecuta desde la raíz del proyecto con:

```bash
python -m src.pipeline
```

La capa Gold (segmentación y métricas derivadas) se documenta en el notebook `04_segmentacion_y_metricas.ipynb`, y el análisis PCA/t-SNE en `05_reduccion_dimensionalidad_pca_tsne.ipynb`.

## Fuente de datos

- Archivo requerido: `data/raw/all_ai_models.csv`
- Origen: dataset "All AI Models" de Epoch AI
- Unidad de análisis: un modelo de IA registrado
- Granularidad esperada: una fila por modelo, después de eliminar duplicados por `Model`

## Resultado de ejecución

El pipeline fue ejecutado con el archivo real `data/raw/all_ai_models.csv`.

| Indicador | Resultado |
|---|---:|
| Filas originales | 3,509 |
| Columnas originales | 57 |
| Filas limpias | 3,405 |
| Columnas limpias | 22 |
| Duplicados por `Model` después de limpiar | 0 |
| Filas con nulos críticos después de limpiar | 0 |
| Año mínimo | 1950 |
| Año máximo | 2026 |

Cobertura de variables numéricas principales:

| Variable | Cobertura |
|---|---:|
| `Parameters` | 65.87% |
| `Training compute (FLOP)` | 40.12% |
| `Training dataset size (total)` | 40.50% |
| `Training time (hours)` | 15.98% |
| `Training compute cost (2023 USD)` | 6.58% |
| `Hardware quantity` | 24.61% |
| `Citations` | 42.94% |

## Reglas de preprocesamiento

Las reglas se trasladan desde el notebook `01_perfilado_y_limpieza.ipynb` y están implementadas en `src/preprocessing.py`:

1. Seleccionar las 20 columnas útiles para identificación, clasificación, escala técnica, costo, hardware, accesibilidad y referencias.
2. Convertir `Publication date` a fecha y derivar `Year` y `Month`.
3. Convertir `Training dataset size (total)` a numérico.
4. Eliminar duplicados por `Model`, conservando el primer registro (6 filas).
5. Eliminar filas sin país, organización o fecha de publicación, porque son dimensiones críticas del análisis (98 filas).
6. En país, categoría de organización y dominio, conservar el primer valor cuando el campo trae categorías separadas por coma.
7. Imputar las categóricas documentadas con `Unknown`.
8. Mantener los nulos numéricos: representan cobertura incompleta de mediciones técnicas y no deben inventarse.

## Opciones de modelo comparadas

### Opción A - Tabla plana

Una sola tabla limpia (`models_flat.csv`) conectable directamente en Tableau. Es simple y útil para exploración rápida, pero mezcla hechos, dimensiones y atributos descriptivos.

Se conserva en el repositorio como fuente de respaldo, validación y comparación directa contra el esquema estrella. También puede usarse en Tableau si se necesita una conexión rápida sin relaciones entre tablas.

### Opción B - Esquema estrella

Una tabla de hechos (`fact_models.csv`) y dimensiones para país, organización, dominio y accesibilidad. Esta estructura reduce repetición y deja relaciones más explícitas para Tableau.

## Métricas de evaluación

Las métricas son de validación estructural, no fórmulas analíticas inventadas:

- cantidad de tablas
- filas en la tabla principal o de hechos
- cantidad de modelos únicos
- duplicados por `Model`
- filas con nulos en campos críticos
- filas con llaves relacionales nulas

## Decisión del modelo

| Opción | Tablas | Filas principales | Modelos únicos | Duplicados por `Model` | Nulos críticos | Llaves relacionales nulas | Recomendación |
|---|---:|---:|---:|---:|---:|---:|---|
| Tabla plana | 1 | 3,405 | 3,405 | 0 | 0 | 0 | Respaldo |
| Esquema estrella | 5 | 3,405 | 3,405 | 0 | 0 | 0 | Seleccionada |

Se recomienda la **Opción B - esquema estrella** porque conserva todas las filas del dataset limpio, mantiene `Model` como llave única de la unidad de análisis y no genera llaves relacionales nulas. La opción plana se mantiene porque es útil para validar totales, revisar discrepancias y conectar rápidamente a Tableau cuando no se requiere modelado relacional.

## Archivos generados

- `data/processed/all_ai_models_clean.csv`
- `outputs/reports/quality_summary.csv`
- `outputs/reports/model_options_comparison.csv`
- `outputs/tableau/models_flat.csv`
- `outputs/tableau/fact_models.csv`
- `outputs/tableau/dim_country.csv`
- `outputs/tableau/dim_organization.csv`
- `outputs/tableau/dim_domain.csv`
- `outputs/tableau/dim_accessibility.csv`
