# The AI Power Map: Visualizando la Geopolítica del Poder Tecnológico Global

**Resumen Ejecutivo**

Equipo: 

Fabian Marcelo Rojas Cuadros, 
Lazaro Machado Luis isaac

Curso: Data Visualization — Universidad Peruana de Ciencias Aplicadas

---

## 1. El problema

La Inteligencia Artificial no se desarrolló de forma distribuida entre países ni organizaciones. Este proyecto analiza 3,405 modelos de IA producidos entre 1950 y 2026 para responder una pregunta central: **¿quién concentra hoy el poder tecnológico de la IA, y qué factores explican esa concentración?**

El análisis está dirigido a investigadores, analistas de política tecnológica y profesionales de datos que necesitan evidencia verificable sobre la estructura real del ecosistema de IA, más allá de titulares periodísticos.

## 2. Fuente de datos

Dataset institucional de Epoch AI ("All AI Models"), con licencia Creative Commons Attribution. Cobertura original de 3,510 registros y 57 variables, reducido tras un proceso de limpieza documentado a 3,405 registros y 22 variables limpias, ampliadas posteriormente a 45 variables analíticas en la capa Gold del pipeline.

## 3. Hallazgos clave

**El poder tecnológico está concentrado en dos bloques, y la brecha es estable en el tiempo.**
Anglosphere concentra el 58% de los modelos producidos (1,991 de 3,405) y China el 25% (847). Juntos representan más del 80% de la producción mundial. El resto del mundo —43 países— se reparte apenas el resto, y Latinoamérica no aparece entre los 15 países con mayor producción. Esta relación de dominancia se mantiene proporcionalmente similar año a año desde 2017 en adelante: el crecimiento exponencial reciente amplificó la brecha en términos absolutos, no la cerró.

**La industria privada desplazó a la academia como motor principal, especialmente desde 2020.**
Hasta la década de 2010, Academia (349 modelos) e Industria (270) producían cantidades similares. En la década de 2020, la Industria produjo 1,801 modelos frente a 677 de la Academia —un crecimiento del 567%—. Globalmente, la Industria concentra el 62.2% de la producción histórica.

**La "apertura" reciente de modelos es en parte engañosa.**
Aunque los modelos abiertos (38.3%) superan levemente a los cerrados (34.9%) en el conteo global, gran parte del crecimiento de "acceso" en la era reciente proviene de la categoría API access, que pasó de 0 a más de 365 modelos solo entre 2023 y 2026. Esto es acceso de uso controlado por la organización, no apertura real de pesos o código —lo cual matiza la narrativa de que la IA se está democratizando.

**El dominio Language desplaza la diversidad tecnológica.**
El 48.4% de todos los modelos pertenecen al dominio de lenguaje, reflejo del boom de LLMs entre 2020 y 2024. En la era más reciente, Language ocupa más espacio que la suma de Visión, Biología y Multimodal combinados, evidenciando una convergencia hacia un solo tipo de arquitectura dominante.

**El análisis de reducción de dimensionalidad (PCA/t-SNE) confirma que la concentración de poder opera sobre volumen de producción, no sobre el tipo de tecnología.**
Al proyectar las características técnicas de los modelos (escala, cómputo, dominio, tipo de organización) en un espacio reducido, los clusters resultantes se agrupan por era tecnológica y por tipo de productor (industria vs. academia), pero **no** se agrupan por bloque geopolítico. Anglosphere y China no ocupan regiones técnicas distintas del espacio de características: compiten en el mismo terreno técnico, no en nichos especializados. Este análisis se aplicó sobre un subconjunto de 632 modelos (18.6% del total) con cobertura completa de variables numéricas clave, limitación reconocida y documentada desde el inicio del proyecto.

## 4. Metodología (resumen)

El proyecto siguió una arquitectura Medallion (Bronze → Silver → Gold): limpieza y corrección de tipos de datos, homologación de categorías con cardinalidad artificialmente inflada, modelado en esquema estrella para Tableau, segmentación por bloque geopolítico, era tecnológica, dominio, organización y accesibilidad, y finalmente un análisis de reducción de dimensionalidad (PCA + t-SNE) sobre variables técnicas estandarizadas. Todas las decisiones de limpieza e imputación se documentaron explícitamente, priorizando la honestidad del dato faltante (etiquetado como "Unknown") sobre la imputación estadística, dado el sesgo que esta última introduciría en variables con distribución muy sesgada.

La estabilidad de los resultados de t-SNE fue verificada ejecutando el algoritmo con una semilla alternativa, confirmando que los patrones observados no son un artefacto de la configuración inicial.

## 5. Limitaciones reconocidas

- El análisis avanzado (PCA/t-SNE) cubre solo 632 de 3,405 modelos (18.6%), sesgado hacia modelos con mejor documentación técnica, típicamente más recientes o notables.
- Variables numéricas clave (Parameters, Training compute, Citations) tienen entre 35% y 60% de nulos y no fueron imputadas, por decisión metodológica explícita.
- El bloque geopolítico no fue usado como variable de entrada en PCA/t-SNE; cualquier patrón geográfico observado es correlación indirecta, no relación estructural directa.

## 6. Conclusión

La evidencia respalda la hipótesis inicial del proyecto: el ecosistema de IA está dominado por dos bloques geopolíticos y por el sector privado, con una brecha que no muestra señales de cerrarse. Sin embargo, el análisis matiza dos supuestos: la apertura de modelos es parcialmente aparente (impulsada por acceso vía API, no por pesos abiertos), y la concentración de poder no se traduce en especialización técnica diferenciada entre bloques —ambos compiten por el mismo tipo de tecnología, a distinta escala de producción.
