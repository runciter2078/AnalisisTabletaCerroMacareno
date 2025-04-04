# Análisis estadístico y de Inteligencia Artificial de la Tableta de Cerro Macareno

**Autor:** Pablo Beret Grande (abril 2025)

---

## Resumen

Este estudio analiza la Tableta de Cerro Macareno mediante técnicas estadísticas e inteligencia artificial. Se transcribieron las marcas de la tablilla, originalmente codificadas en múltiples estados, y se simplificaron a un modelo que conserva tres estados: **vertical**, **horizontal** y **vacío**. Se aplicaron métodos de autocorrelación espacial, transformada de Fourier (FFT), reducción de dimensionalidad (PCA y t-SNE) y clustering difuso (Fuzzy C-means) para explorar la estructura subyacente y evaluar la influencia de la orientación de lectura.

**Palabras clave:** Tableta de Cerro Macareno, análisis estadístico, inteligencia artificial, autocorrelación espacial, FFT, PCA, t-SNE, clustering difuso, arqueología, patrones astronómicos.

---

## Abstract

This study analyzes the Tableta de Cerro Macareno using statistical and artificial intelligence techniques. The tablet markings, originally encoded in multiple states, are simplified to a model that preserves three states: vertical, horizontal, and blank. Spatial autocorrelation, Fourier transform (FFT), dimensionality reduction (PCA and t-SNE), and fuzzy clustering (Fuzzy C-means) methods are applied to explore the underlying structure and assess the impact of reading orientation.

**Key Words:** Tableta de Cerro Macareno, statistical analysis, artificial intelligence, spatial autocorrelation, FFT, PCA, t-SNE, fuzzy clustering, archaeology, astronomical patterns.

---

## Introducción

La Tableta de Cerro Macareno es un artefacto arqueológico cuya función y significado han generado múltiples hipótesis. En este estudio se transcribieron las marcas de la tablilla, inicialmente codificadas en varios estados (vertical, horizontal, inclinaciones a la derecha e izquierda, etc.), y se aplicaron técnicas estadísticas y de inteligencia artificial para determinar la estructura subyacente. Los análisis revelaron que, para fines prácticos, el sistema se comporta de forma binaria (vertical vs. horizontal), manteniéndose la categoría de casillas en blanco. Además, se evaluó la influencia de la orientación de lectura (horizontal vs. vertical) mediante métodos de autocorrelación espacial, FFT, PCA, t-SNE y clustering difuso.

---

## Historia y Contexto

La Tableta fue hallada en el yacimiento del Cerro Macareno, en la provincia de Sevilla, y ha suscitado debate sobre su función. Diversas interpretaciones sugieren que podría tratarse de un registro de sucesos, un inventario o incluso un proto-sistema de escritura. Ante la ausencia de un corpus comparativo amplio, este estudio se centra en analizar la distribución de las marcas para evaluar si existe una organización intencional y, potencialmente, si se asocia a patrones de origen astronómico o a registros de fenómenos temporales y espaciales.

---

## Metodología

### Transcripción y Codificación de Datos

Se identificaron inicialmente múltiples categorías en las marcas:

- **1:** Raya vertical  
- **1.5:** Raya ligeramente inclinada hacia la derecha  
- **2:** Raya inclinada a aproximadamente 45º hacia la derecha  
- **3:** Raya horizontal  
- **3.5:** Raya ligeramente inclinada hacia la izquierda  
- **4:** Raya inclinada a aproximadamente 45º hacia la izquierda  
- **5:** Vacío

Tras los análisis preliminares se comprobó que la variabilidad se reduce a una distinción fundamental:

- **Vertical:** asignación numérica 1 (valores menores a un umbral, por ejemplo, < 2.5)
- **Horizontal:** asignación numérica 3 (valores ≥ 2.5)

Esta transformación a un modelo “binario” (conservando los vacíos representados por el 5) simplifica la interpretación y permite detectar patrones estructurales.

> **Ejemplo del DataFrame original (orientación horizontal):**  
> ![DataFrame original (horizontal)](https://github.com/runciter2078/AnalisisTabletaCerroMacareno/blob/main/data/dataframe_original_horizontal.png?raw=true)

### Análisis Estadísticos y de IA Aplicados

#### 1. Autocorrelación Espacial

Se evaluó la estructura espacial mediante:
- **Sumas por filas y columnas:** que actúan como indicadores de la distribución de estados.
- **Promedio de vecinos (vecindad de Moore):** para cada celda se calcula el promedio de sus 8 vecinos.
- **Coeficiente de correlación de Pearson:**

\[
r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}
\]

donde \(x_i\) es el valor de la celda y \(y_i\) el promedio de sus vecinos. Los análisis arrojaron un coeficiente moderado, indicando que la distribución no es aleatoria.

#### 2. Transformada de Fourier (FFT)

La FFT se utilizó para detectar periodicidades en las sumas por filas y columnas. Se define como:

\[
X(k) = \sum_{n=0}^{N-1} x(n)\,e^{-i\,2\pi\frac{k\,n}{N}}
\]

Esta herramienta permite identificar posibles ciclos o patrones repetitivos que, en una hipótesis astronómica, podrían relacionarse con ciclos temporales (por ejemplo, lunar o solar). Aunque se graficaron los espectros, no se detectaron picos de periodicidad claramente marcados.

#### 3. Reducción de Dimensionalidad: PCA y t-SNE

- **PCA (Análisis de Componentes Principales):**  
  Se emplea para reducir la dimensionalidad del conjunto de datos y extraer las direcciones de mayor varianza. El método transforma el conjunto de datos \(X\) en un conjunto de componentes \(Z\) utilizando la matriz de covarianza.

- **t-SNE:**  
  Técnica no lineal que permite visualizar agrupamientos latentes en datos de alta dimensión. Dada la limitada cantidad de muestras (por ejemplo, 8 filas), se ajustaron parámetros como el _perplexity_ para obtener visualizaciones coherentes.

Ambas técnicas evidenciaron agrupaciones latentes en la distribución de los estados, lo que respalda la robustez estructural de la Tableta.

#### 4. Clustering Difuso: Fuzzy C-means

El clustering difuso permite asignar a cada celda grados de pertenencia a distintos clusters. El algoritmo Fuzzy C-means minimiza la función objetivo:

\[
J_m = \sum_{i=1}^{N} \sum_{j=1}^{C} u_{ij}^m \| x_i - c_j \|^2
\]

donde \(u_{ij}\) es el grado de pertenencia de la muestra \(x_i\) al cluster \(j\), \(c_j\) es el centro del cluster, y \(m\) es el coeficiente de fuzzificación. El Fuzzy Partition Coefficient (FPC) se utiliza para evaluar la calidad de la partición; valores cercanos a 1 indican una partición nítida. En el análisis se obtuvo un FPC de aproximadamente 0.70 para \(k=2\), lo que sugiere una división robusta en dos bloques.

#### 5. (Opcional) Transformación PCA Básica

Para una representación simplificada de la transformación PCA se puede usar:

\[
Z = XW
\]

donde \(W\) son los vectores propios de la matriz de covarianza de \(X\).

#### 6. Orientación de Lectura

Se realizaron los análisis tanto en la orientación **horizontal** (tal como se transcribió originalmente) como en la orientación **vertical** (tras transponer la matriz). Esto permite evaluar si la dirección de lectura afecta la interpretación de la estructura.

---

## Resultados

### Orientación Horizontal

- **Sumas por Filas y Columnas:**  
  Las sumas varían en cada fila y columna, lo que sugiere la existencia de bloques diferenciados.

- **Autocorrelación Espacial:**  
  Se obtuvo un coeficiente de correlación de Pearson moderado, lo que indica que celdas con valores similares tienden a agruparse.

- **FFT:**  
  Los espectros obtenidos no muestran periodicidades marcadas, aunque permiten descartar la presencia de ciclos evidentes.

- **Reducción de Dimensionalidad (PCA y t-SNE):**  
  - La PCA muestra indicios de dos agrupaciones, aunque la separación no es muy nítida.  
  - El t-SNE evidencia agrupamientos más claros, lo que confirma la robustez de la estructura.

- **Clustering Difuso:**  
  Con \(k=2\), el Fuzzy C-means produjo una partición robusta (FPC ≈ 0.70) que sugiere la existencia de dos secciones diferenciadas.

> **Gráficas representativas (Orientación Horizontal):**  
> - FFT de filas y columnas  
> - PCA y t-SNE  
> - Resultados del clustering difuso  
> *(Ver imágenes en la carpeta [data](https://github.com/runciter2078/AnalisisTabletaCerroMacareno/tree/main/data))*

### Orientación Vertical

Para simular la lectura vertical se transpusó la matriz (intercambiando filas y columnas). Se aplicaron los mismos análisis:

- **Sumas por Filas y Columnas:**  
  La distribución sigue presentando dos modos, similar a la orientación horizontal.

- **Autocorrelación Espacial y FFT:**  
  Los cálculos de sumas y la FFT muestran resultados comparables a la orientación horizontal; es decir, sin picos de periodicidad claramente marcados, pero confirmando patrones de distribución.

- **Reducción de Dimensionalidad (PCA y t-SNE):**  
  - La PCA indica dos tendencias principales, aunque la separación es menos pronunciada en algunos casos.  
  - El t-SNE en orientación vertical en ocasiones revela una agrupación casi perfecta en dos bloques, lo que podría sugerir que la lectura vertical resalta de forma más clara la segmentación o bien, ofrece una perspectiva complementaria.

- **Clustering Difuso:**  
  El Fuzzy C-means para \(k=2\) produjo un FPC similar (≈ 0.70), confirmando la robustez de la partición en ambas orientaciones.

> **Gráficas representativas (Orientación Vertical):**  
> - FFT de filas y columnas  
> - PCA y t-SNE  
> - Resultados del clustering difuso  
> *(Ver imágenes en la carpeta [data](https://github.com/runciter2078/AnalisisTabletaCerroMacareno/tree/main/data))*

---

## Conclusiones

Los análisis realizados indican que la Tableta de Cerro Macareno presenta una organización no aleatoria, con bloques diferenciados que se mantienen consistentes en ambas orientaciones (horizontal y vertical). La transformación a un modelo que conserva tres estados (1 = vertical, 3 = horizontal, 5 = vacío) simplifica la interpretación, mostrando que las marcas se agrupan fundamentalmente en estos estados.

- **Orientación Horizontal:**  
  Los métodos de autocorrelación, FFT, PCA, t-SNE y clustering difuso evidencian la existencia de dos agrupaciones principales. Aunque la FFT no reveló periodicidades marcadas, los patrones espaciales y la robustez del clustering respaldan la hipótesis de una estructura intencional.

- **Orientación Vertical:**  
  Los resultados son comparables a los obtenidos en orientación horizontal. En particular, el t-SNE en ciertos ensayos mostró una separación casi perfecta en dos bloques, lo que podría indicar que la lectura vertical resalta de forma más clara la segmentación o, al menos, aporta una visión complementaria. En cualquier caso, ambos enfoques confirman la solidez de la estructura subyacente.

En conjunto, la convergencia de estos distintos enfoques analíticos respalda la transformación a un modelo binario (manteniendo los vacíos) y sugiere que la Tableta podría haber sido utilizada para registrar información espacial o temporal. Esto abre la puerta a futuras investigaciones, incluyendo comparaciones con datos astronómicos y el análisis de otros artefactos arqueológicos.

---

## Referencias

- **Transformada de Fourier:**  
  Bracewell, R. N. *The Fourier Transform and Its Applications*.

- **PCA:**  
  Jolliffe, I. *Principal Component Analysis*.

- **t-SNE:**  
  van der Maaten, L., & Hinton, G. *Visualizing Data using t-SNE*.

- **Fuzzy C-means:**  
  Bezdek, J. C. *Pattern Recognition with Fuzzy Objective Function Algorithms*.
