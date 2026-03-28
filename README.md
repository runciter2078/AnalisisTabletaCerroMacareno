# Análisis estadístico de la Tableta de Cerro Macareno

**Autor:** Sergio Pablo Beret Grande  
**Afiliación:** Investigador independiente; doctorando, Universidad Internacional de Valencia (afiliación solo a efectos de identificación)  
**Fecha:** Marzo 2026  

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19285307.svg)](https://doi.org/10.5281/zenodo.19285307)

---

## Descripción

Este repositorio contiene el análisis estadístico completo de la **Tableta de Cerro Macareno**, una pieza de barro cocido (8 filas × 14 columnas = 112 casillas) conservada en el Museo Arqueológico de Sevilla (inventario CE14568), hallada en el yacimiento de La Rinconada (Sevilla, España).

El análisis extiende el trabajo previo de Sáez Uribarri (2006) con estadística espacial moderna, análisis espectral, tests de hipótesis astronómicas y aprendizaje automático exploratorio.

El **preprint** está publicado en Zenodo:  
> Beret Grande, S.P. (2026). *Statistical Analysis of the Cerro Macareno Tablet: Non-Random Structure, Spatial Gradients, and Astronomical Exploration*. Zenodo.  
> https://doi.org/10.5281/zenodo.19285307

---

## Conclusiones principales

### ✅ Hallazgos establecidos con certeza estadística

| Resultado | Test | Estadístico |
|---|---|---|
| Gradiente izquierda-derecha | Fisher exact | OR = 7.58, p = 7×10⁻⁶ |
| No independencia secuencial | Runs test (3 linealizaciones) | p < 0.005 en todas |
| F7–F8 no son incompletas | Mann-Whitney + t-test | p = 0.833 / p = 0.831 |

El ~69 % de los eventos (marcas verticales) se concentran en las columnas C1–C5. Esta es la característica estructural dominante del artefacto.

### ⚠️ Hallazgos que requieren interpretación cautelosa

- **Moran's I:** I = 0.245, significativo bajo nulo libre (p < 0.001), pero p ≈ 0.17 bajo nulo fixed-margin. La autocorrelación local no está establecida más allá del gradiente.
- **Periodicidad T = 14:** Picos ACF en lags 14, 28, 42. Sin embargo, T = 14 coincide exactamente con la longitud de fila, por lo que puede ser un artefacto de la linealización. El periodograma FFT no confirma el pico.

### 🔭 Exploración astronómica (hipótesis compatible, no confirmada)

- **Fase 4d** (test maxT, nulo fixed-margin, 9 999 permutaciones Curveball): p = 0.034 [IC 95 %: 0.031–0.038]. Existe una asociación estructurada residual más allá del gradiente fila+columna que es capturada por un modelo de elongaciones de Venus. Mejor ancla: ~573 a.C.
- **Fases 4e y 4e-bis** (validación LORO contra 9 controles periódicos): Venus queda **#9 de 10** en ganancia predictiva fuera de muestra. Los tres controles de mayor rango (P = 780d, P = 900d, P = 400d) tienen Δlog-lik medio positivo; Venus no.

**Veredicto:** Los datos son compatibles con la hipótesis de Venus pero no la identifican como la explicación periódica única o mejor sustentada. Con 112 casillas y 32 eventos el poder estadístico es insuficiente para discriminar entre hipótesis astronómicas alternativas.

---

## Estructura del repositorio
```
AnalisisTabletaCerroMacareno/
│
├── data/
│   ├── tableta.xlsx          # Codificación de la matriz (fuente primaria)
│   ├── tablilla.jpg          # Fotografía del artefacto
│   ├── tablilla_2.png
│   └── tablilla_saez_2006.jpg
│
├── notebooks/
│   └── 01_tableta_macareno.ipynb   # Notebook principal (143 celdas, 6 fases + 4b/4c/4d/4e/4e-bis)
│
├── scripts/
│   ├── fase4d_maxT_structured.py         # Test maxT con nulo fixed-margin (Fase 4d)
│   ├── fase4e_specificity_LORO.py        # Especificidad Venus vs pseudo-Venus (Fase 4e)
│   └── fase4ebis_specificity_calibrated.py  # LORO con calibración de densidad (Fase 4e-bis)
│
├── results/
│   ├── fig01–fig26_*.png     # Figuras Fases 1–4c
│   ├── fig27_fase4d_maxT_structured.png
│   ├── fig28_fase4e_LORO_specificity.png
│   ├── fig29_fase4ebis_calibrated.png
│   ├── fase4d_resultados.npy
│   ├── fase4e_resultados.npy
│   └── fase4ebis_resultados.npy
│
├── paper/
│   └── cerro_macareno_2026.pdf   # Preprint publicado (DOI: 10.5281/zenodo.19285307)
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## Reproducibilidad
```bash
conda activate macareno
jupyter lab notebooks/01_tableta_macareno.ipynb
# Kernel → Restart & Run All
```

**Entorno:** Python 3.11 · NumPy 2.4 · SciPy 1.17 · scikit-learn 1.8 · statsmodels 0.14 · libpysal · esda · Skyfield 1.46  
**Efemérides:** JPL DE406 (`de406.bsp`, ~190 MB, se descarga automáticamente en la primera ejecución)  
**Semilla global:** `RANDOM_SEED = 42`

> **Nota:** Los archivos de efemérides (`.bsp`) están excluidos del repositorio por su tamaño. Se descargan automáticamente al ejecutar las fases 4b, 4c, 4d, 4e y 4e-bis.

---

## Fases del análisis

| Fase | Contenido |
|---|---|
| 1 | Datos canónicos, exploración visual, estadísticas descriptivas |
| 2 | Tests de no-aleatoriedad: permutación MI, runs tests, Fisher exact, Moran's I, LISA |
| 3 | Análisis espectral: FFT, ACF/PACF, wavelet de Morlet |
| 4 | Contraste hipótesis astronómicas (modelos sintéticos) |
| 4b | Contraste con efemérides reales JPL/DE406, búsqueda de fecha óptima |
| 4c | Modelo de posición sinódica de Venus (elongaciones máximas exactas) |
| 4d | Test maxT con nulo estructurado fixed-margin (Curveball) |
| 4e | Especificidad Venus vs pseudo-Venus — validación LORO |
| 4e-bis | LORO con calibración de densidad + Venus+jitter |
| 5 | ML exploratorio: Fuzzy C-means, HMM, PELT |
| 6 | Síntesis de evidencia y conclusiones finales |

---

## Referencia
```bibtex
@misc{beretgrande2026macareno,
  author    = {Beret Grande, Sergio Pablo},
  title     = {Statistical Analysis of the Cerro Macareno Tablet:
               Non-Random Structure, Spatial Gradients, and Astronomical Exploration},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.19285307},
  url       = {https://doi.org/10.5281/zenodo.19285307}
}
```

---

## Licencia

Este repositorio se distribuye bajo licencia [MIT](LICENSE).  
El preprint está publicado bajo [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).