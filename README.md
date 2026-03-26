# Análisis estadístico y de inteligencia artificial aplicado a la Tableta de Cerro Macareno

**Autor:** Pablo Beret Grande  
**Repositorio:** https://github.com/runciter2078/AnalisisTabletaCerroMacareno  
**Fecha:** 2026  
**Entorno:** Python 3.11 · NumPy 2.4 · SciPy 1.17 · ver `environment.yml`

---

## Descripción

La **Tableta de Cerro Macareno** es una pieza de barro cocido conservada en el Museo Arqueológico de Sevilla, hallada en el yacimiento homónimo de La Rinconada (Sevilla, España). Contiene una cuadrícula de **8 filas × 14 columnas** (112 casillas) con muescas verticales, horizontales, oblicuas o espacios en blanco, cuya función y cronología han permanecido sin resolver desde su descripción original (Fernández et al., 1979).

Este proyecto aplica estadística moderna, análisis espacial, análisis espectral, contraste de hipótesis astronómicas e inteligencia artificial (Fuzzy C-means, HMM, detección de cambio estructural) para responder tres preguntas fundamentales:

1. ¿Es la distribución de marcas aleatoria o tiene estructura?
2. ¿Qué tipo de estructura tiene y cuál es su periodo dominante?
3. ¿Es la distribución compatible con algún fenómeno periódico externo —astronómico o natural?

El análisis parte de la codificación y conclusiones de **Sáez Uribarri (2006)** como base, y las amplía con métodos cuantitativos independientes y modernos.

> **Apoyo metodológico:** Este análisis se desarrolló con el apoyo de [Claude](https://claude.ai) (Anthropic) como asistente de ciencia de datos, utilizado a través de Claude.ai.

---

## Resultados principales

### 1. La tableta NO es aleatoria — evidencia fuerte

6 de 7 tests independientes rechazan la hipótesis nula de aleatoriedad tras corrección FDR (Benjamini-Hochberg, α=0.05):

| Test | Estadístico | p-valor |
|------|-------------|---------|
| Permutation test (MI vecinal) | MI_obs = 0.059 vs pct95_nulo = 0.010 | < 0.0001 |
| Runs test L1 (fila a fila) | Z = −3.20 | 0.0014 |
| Runs test L2 (columna a columna) | Z = −3.66 | 0.0003 |
| Runs test L3 (zigzag) | Z = −3.20 | 0.0014 |
| Test de Fisher (izq. vs der.) | OR = 7.58 | 7.0 × 10⁻⁶ |
| Moran's I global | I = 0.245, z = 5.02 | 0.0001 |

### 2. El gradiente izquierda-derecha es la señal más robusta

La densidad de eventos verticales en las columnas C1–C5 es **3.96 veces mayor** que en C6–C14 (Fisher OR = 7.58, p = 7 × 10⁻⁶). El mapa LISA identifica 12 clusters HH significativos concentrados en C2–C5, filas F3–F8. Esta estructura es incompatible con distribución aleatoria y con escritura fonética o silábica.

### 3. Periodicidad dominante T ≈ 14 celdas

Los lags 14, 28 y 42 de la ACF son significativos (tres múltiplos consecutivos). El análisis wavelet de Morlet muestra una banda estacionaria en T ≈ 14 a lo largo de toda la secuencia. Bajo la hipótesis de escala mensual (1 celda = 1 mes sinódico), T = 14 celdas ≈ 1.13 años tropicales, coherente con una estructura de 8 años registrada en 14 unidades sub-anuales por fila.

> **Nota:** El periodograma de potencia no supera el umbral de significación por un artefacto matemático: N = 112 = 8 × 14 hace que el test de permutación circular sea ciego al período T = 14. La evidencia de periodicidad se basa en la ACF y la wavelet.

### 4. El perfil mensual es compatible con Venus y eclipses, pero NO con un ciclo anual genérico

Test A (permutación de columnas, 14 puntos, 9999 muestras):

| Hipótesis | r | p-valor |
|-----------|---|---------|
| H1: Venus (elongaciones máx.) | 0.580 | **0.021** ✓ |
| H2a: Eclipses (densidad obs.) | 0.545 | **0.033** ✓ |
| H2b: Eclipses (estructura Saros) | 0.526 | **0.019** ✓ |
| H3a: Ciclo anual genérico | 0.427 | 0.065 |
| H3b: Ciclo anual ajustado | 0.427 | 0.069 |

La discriminación entre H1/H2 (significativos) y H3 (no significativo) indica que la compatibilidad no es simplemente "cualquier cosa periódica", sino que el perfil específico de la tableta se asemeja más al de Venus y eclipses que al de una sinusoide anual. Esta conclusión se basa en modelos matemáticos, no en efemérides retrocalculadas para Sevilla. Para una afirmación definitiva se requieren datos NASA/JPL para 37°N, 5.9°W en el rango 800–200 a.C.

### 5. F7–F8 son posicionalmente distintas, no incompletas

Contrariamente a la hipótesis de Sáez Uribarri (2006), las filas 7–8 **no tienen menor densidad** que las filas 1–6 (Mann-Whitney p = 0.833). Su densidad media (0.357) es superior a la de F1–F6 (0.262). Lo que las distingue es su patrón posicional: todos sus eventos caen en C2–C5 sin excepciones, con la mayor consistencia interna de cualquier par de filas. El FCM las agrupa en un cluster propio (membresía = 1.00 en ambas). **F1, con solo 1 evento en C14 (patrón invertido), es el verdadero outlier de la tableta.**

### 6. Análisis ML: estructura interna real

- **Fuzzy C-means:** todos los c = 2..5 son significativos frente al nulo (p ≤ 0.005). c = 5 produce agrupaciones con membresía alta (F1, F4, F7, F8 con membresía = 1.00 en sus respectivos clusters), indicando estructura no intercambiable entre filas.
- **HMM 2 estados:** LRT significativo (χ² = 10.88, df = 4, p = 0.028). Estado activo P(evento) = 0.78, estado pasivo P(evento) = 0.00. Captura la autocorrelación local entre celdas adyacentes.
- **Pelt BIC:** sin breakpoints en la secuencia completa. No hay una ruptura única sino variabilidad distribuida entre filas.

---

## Estructura del repositorio

```
AnalisisTabletaCerroMacareno/
│
├── data/
│   ├── tableta.xlsx              # Codificación Sáez Uribarri (2006)
│   ├── tablilla.jpg              # Fotografía de la tableta
│   ├── tablilla_saez_2006.jpg    # Esquema de referencia (SPAL 2006)
│   └── tablilla_2.png            # Imagen alternativa
│
├── notebooks/
│   └── 01_tableta_macareno.ipynb # Notebook principal (6 fases, 23 figuras)
│
├── results/                      # Figuras generadas (PNG, 300 DPI)
│   ├── fig01_tableta_imagen.png
│   ├── fig02_heatmaps.png
│   ├── ...
│   └── fig23_sintesis_evidencia.png
│
├── README.md
├── LICENSE
└── .gitignore
```

---

## Fases del análisis

| Fase | Contenido | Figuras |
|------|-----------|---------|
| **1** | Datos canónicos, matrices M_raw y M_bin, exploración visual, gradiente L→R, secuencia linealizada, entropía | 1–7 |
| **2** | Tests de no-aleatoriedad: permutation test MI, runs test ×3, Fisher, Moran's I, LISA; corrección FDR-BH | 8–11 |
| **3** | Análisis espectral: periodograma FFT, permutación circular, ACF/PACF, wavelet Morlet, robustez L1 vs L2 | 12–15 |
| **4** | Contraste hipótesis externas (Venus, eclipses, anual, columnar): cross-correlación FFT, Test A columnar, Test B bootstrap | 16–19 |
| **5** | ML exploratorio: Fuzzy C-means (c=2..5), HMM 2 estados, detección cambio estructural Pelt | 20–22 |
| **6** | Síntesis de evidencia, tabla maestra, conclusiones finales, estadísticos de referencia | 23 |

---

## Reproducibilidad

### Requisitos

```bash
# Crear entorno conda
conda create -n macareno python=3.11 numpy="1.26" pandas scipy scikit-learn \
    matplotlib seaborn statsmodels jupyterlab ipykernel -c conda-forge -y

conda activate macareno

pip install scikit-fuzzy hmmlearn ruptures esda libpysal openpyxl
```

### Ejecución

```bash
conda activate macareno
jupyter lab notebooks/01_tableta_macareno.ipynb
# Kernel → Restart & Run All
```

Todas las figuras se generan automáticamente en `results/`. La semilla aleatoria global es `RANDOM_SEED = 42`. Los modelos nulos usan `np.random.default_rng(RANDOM_SEED + k)` con `k` distinto por bloque para garantizar independencia entre tests. El tiempo total de ejecución es aproximadamente 15–25 minutos (dominado por los permutation tests de Fase 4 y FCM de Fase 5).

### Estadísticos clave de referencia rápida

| Estadístico | Valor |
|-------------|-------|
| N total | 112 celdas (8 × 14) |
| Eventos (verticales) | 32 / 112 (28.6%) |
| Gradiente C1-5 / C6-14 | 3.96× |
| Fisher OR | 7.58 (p = 7.0 × 10⁻⁶) |
| Moran's I | 0.245 (z = 5.02, p = 0.0001) |
| Período ACF dominante | T = 14 celdas (lags 14, 28, 42) |
| Test A Venus | r = 0.580 (p = 0.021) |
| Test A Saros | r = 0.526 (p = 0.019) |
| Test A Anual genérico | r = 0.427 (p = 0.065, no sig.) |
| HMM LRT | χ² = 10.88, df = 4, p = 0.028 |
| FCM c=2 FPC | 0.666 (p = 0.005) |
| F7-F8 vs F1-F6 density | Mann-Whitney p = 0.833 (no sig.) |

---

## Líneas de trabajo futuro

**(a) Efemérides reales:** Usar datos NASA/JPL (HORIZONS) retrocalculados para Sevilla (37°N, 5.9°W) en el rango 800–200 a.C. para un contraste puntual no circular con poder estadístico real.

**(b) Comparativa regional:** Buscar patrones similares en otras tabletas del Mediterráneo occidental del mismo período (Tartessos, Fenicia ibérica, sur de Portugal).

**(c) Imagen multiespectral:** Solicitar al Museo Arqueológico de Sevilla un estudio de imagen multiespectral de la pieza física para detectar marcas adicionales no visibles en las fotografías disponibles.

**(d) Codificación ternaria completa:** Analizar la distinción entre horizontal (3) y blanco (5) mediante modelos de Markov de orden superior o redes bayesianas, en lugar de colapsar ambos en "no-evento".

---

## Referencia base

Sáez Uribarri, I. (2006). La tableta de Cerro Macareno: Análisis exploratorio de datos en torno a una pieza de arqueología. *SPAL: Revista de Prehistoria y Arqueología*, 15, 11–26. © 2006 SPAL. Licencia CC BY-NC-ND 4.0. DOI: [10.12795/spal.2006.i15.01](https://revistascientificas.us.es/index.php/spal/article/view/11614)

Fernández, F.; Chasco, V. y Oliva, D. (1979). Excavaciones en el "Cerro Macareno", La Rinconada (Sevilla). *Noticiario Arqueológico Hispánico*, 7, 10–93.

---

## Licencia

MIT — ver [LICENSE](LICENSE)

---

## Cómo citar este trabajo

```
Beret Grande, P. (2026). Análisis estadístico y de inteligencia artificial
aplicado a la Tableta de Cerro Macareno [Software].
GitHub: https://github.com/runciter2078/AnalisisTabletaCerroMacareno
```
