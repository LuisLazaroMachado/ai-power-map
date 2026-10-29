# Datos

## Fuente

Los datos provienen del dataset **All AI Models** de Epoch AI, el registro de modelos de aprendizaje automático que sigue la evolución de la IA (https://epoch.ai/data/ai-models).

Cita sugerida por Epoch AI:

> Epoch AI, "Data on AI Models". Publicado en línea en epoch.ai. Recuperado de https://epoch.ai/data/ai-models-documentation

## Licencia

Los datos de Epoch AI se distribuyen bajo la licencia [Creative Commons Attribution 4.0 (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/): se pueden usar, distribuir y reproducir citando la fuente y a sus autores.

## Contenido y modificaciones

| Carpeta | Contenido | Relación con el original |
|---|---|---|
| `raw/` | `all_ai_models.csv` (3,509 filas × 57 columnas) | Copia sin modificar |
| `processed/` | `all_ai_models_clean.csv` (3,405 filas × 22 columnas) | **Modificado**: selección de columnas, deduplicación por `Model`, eliminación de filas sin país, organización o fecha, homologación de categorías e imputación de categóricas con `Unknown` |

Las tablas de `outputs/` también son derivadas de estos datos (esquema estrella, segmentaciones, métricas y coordenadas PCA/t-SNE). Conservan la atribución a Epoch AI y se comparten bajo los mismos términos CC BY 4.0. Las reglas exactas están en [`docs/modelo_de_datos_y_preprocesamiento.md`](../docs/modelo_de_datos_y_preprocesamiento.md).
