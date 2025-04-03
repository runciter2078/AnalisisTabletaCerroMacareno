# Análisis Estadístico y de IA de la Piedra de Cerro Macareno

Autor: Pablo Beret Grande (abril 2025)

## Introducción

La Piedra de Cerro Macareno es un artefacto arqueológico cuya función y significado han generado múltiples hipótesis. En este estudio se transcribieron las marcas de la tablilla, inicialmente codificadas en varios estados (vertical, horizontal, inclinaciones a la derecha e izquierda, etc.), y se aplicaron técnicas estadísticas y de inteligencia artificial para determinar la estructura subyacente. Los análisis revelaron que, para fines prácticos, el sistema se comporta de forma binaria (vertical vs. horizontal). Se evaluó además la influencia de la orientación de lectura (horizontal vs. vertical) mediante métodos de correlación espacial, transformada de Fourier (FFT), reducción de dimensionalidad (PCA y t-SNE) y clustering difuso (Fuzzy C-means).

## Historia y Contexto

La piedra fue hallada en el yacimiento del Cerro Macareno, en la provincia de Sevilla, y forma parte de los objetos arqueológicos que han suscitado debate sobre su función. Diversas interpretaciones han sugerido que podría tratarse de un registro de sucesos, un inventario o incluso un proto-sistema de escritura. Ante la falta de un corpus comparativo amplio, se ha optado por analizar la distribución de las marcas en la pieza, para evaluar si existe una organización intencional y, potencialmente, si se asocia a patrones de origen astronómico o a registros de fenómenos temporales o espaciales.

## Metodología

### Transcripción y Codificación de Datos

Inicialmente se identificaron múltiples categorías en las marcas:
- **1:** Raya vertical
- **1.5:** Raya ligeramente inclinada hacia la derecha
- **2:** Raya inclinada a aproximadamente 45º hacia la derecha
- **3:** Raya horizontal
- **3.5:** Raya ligeramente inclinada hacia la izquierda
- **4:** Raya inclinada a aproximadamente 45º hacia la izquierda
- **5:** Vacío

Tras los análisis preliminares, se comprobó que la variabilidad se reduce a una distinción fundamental:  
- **Vertical:** asignación numérica 1 (valores menores a un umbral, por ejemplo, < 2.5)  
- **Horizontal:** asignación numérica 3 (valores ≥ 2.5)

Esta transformación a modelo binario simplifica la interpretación y posibilita la detección de patrones estructurales.

### Análisis Estadísticos y de IA Aplicados

#### 1. Autocorrelación Espacial

Para evaluar la estructura espacial, se calculan:
- **Sumas por filas y columnas:** Indicadores de la distribución de estados.
- **Promedio de vecinos (vecindad de Moore):** Para cada celda se calcula el promedio de los 8 vecinos.
- **Coeficiente de correlación de Pearson:**  
  $$
  r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}
  $$
  donde \( x_i \) es el valor de la celda y \( y_i \) el promedio de sus vecinos. Los análisis arrojaron un coeficiente moderado, indicando que la distribución no es aleatoria.

#### 2. Transformada de Fourier (FFT)

La FFT se utiliza para detectar periodicidades en las sumas por filas y columnas. La transformada se define como:
$$
X(k) = \sum_{n=0}^{N-1} x(n)\, e^{-i\, 2\pi \frac{k\, n}{N}}
$$
Esta herramienta permite identificar posibles ciclos o patrones repetitivos que, en una hipótesis astronómica, podrían relacionarse con ciclos temporales (por ejemplo, lunar o solar). En este caso, aunque se han calculado y graficado los espectros, no se detectaron picos de periodicidad claramente marcados.

#### 3. Reducción de Dimensionalidad: PCA y t-SNE

- **PCA (Análisis de Componentes Principales):**  
  Se emplea para reducir la dimensionalidad del conjunto de datos y extraer las direcciones de mayor varianza. El método transforma el conjunto de datos \( X \) en un conjunto de componentes \( Z \) mediante la matriz de covarianza.
- **t-SNE:**  
  Técnica no lineal de reducción de dimensionalidad que permite visualizar agrupamientos latentes en datos de alta dimensión. Dada la escasez de muestras (por ejemplo, 8 filas), se ajustaron parámetros como el _perplexity_ para obtener visualizaciones coherentes.

Ambas técnicas han evidenciado agrupaciones latentes en la distribución de los estados, lo que respalda la robustez estructural de la piedra.

#### 4. Clustering Difuso: Fuzzy C-means

El clustering difuso permite que cada celda tenga grados de pertenencia a distintos clusters. El algoritmo Fuzzy C-means minimiza la función objetivo:
$$
J_m = \sum_{i=1}^{N} \sum_{j=1}^{C} u_{ij}^m \| x_i - c_j \|^2
$$
donde \( u_{ij} \) es el grado de pertenencia de la muestra \( x_i \) al cluster \( j \), \( c_j \) es el centro del cluster y \( m \) es el coeficiente de fuzzificación. El Fuzzy Partition Coefficient (FPC) se utiliza para evaluar la calidad de la partición; valores cercanos a 1 indican una partición nítida. En el análisis, se obtuvo un FPC de aproximadamente 0.70 para \( k=2 \), lo que sugiere una división robusta en dos bloques.

### Orientación de Lectura

Se realizaron los análisis tanto en la orientación horizontal (como se transcribió originalmente) como en la orientación vertical (tras transponer la matriz). Los resultados en ambas orientaciones fueron consistentes, indicando que la estructura subyacente de la piedra es robusta y no depende de la dirección de lectura.

## Resultados

- **Suma de Filas y Columnas:**  
  Las sumas varían en cada fila y columna, lo que sugiere la existencia de bloques diferenciados.

- **Autocorrelación Espacial:**  
  Se obtuvo un coeficiente de correlación de Pearson moderado, respaldado por el análisis de promedios de vecinos, lo que indica que celdas con valores similares tienden a agruparse.

- **FFT:**  
  Los espectros obtenidos no muestran periodicidades claramente marcadas, aunque la herramienta es útil para descartar la presencia de ciclos evidentes.

- **PCA y t-SNE:**  
  Ambas técnicas revelaron agrupaciones latentes en la distribución de las celdas, confirmando la robustez de la estructura, independientemente de la orientación.

- **Clustering Difuso:**  
  Con \( k=2 \), el Fuzzy C-means produjo una partición robusta (FPC ≈ 0.70) que sugiere la existencia de dos secciones diferenciadas, interpretables como la presencia versus la ausencia de un fenómeno registrado.

## Conclusiones

Los análisis realizados indican que la Piedra de Cerro Macareno presenta una organización no aleatoria, con bloques diferenciados que se mantienen consistentes en ambas orientaciones (horizontal y vertical). La transformación a un modelo binario simplifica la interpretación, mostrando que las marcas se agrupan fundamentalmente en dos estados (vertical y horizontal). Esta partición robusta, evidenciada mediante autocorrelación espacial, técnicas de reducción de dimensionalidad y clustering difuso, abre la posibilidad de interpretar estos bloques como registros diferenciados (por ejemplo, presencia versus ausencia de un fenómeno). Aunque no se detectaron periodicidades astronómicas evidentes, la existencia de una estructura ordenada sugiere que la piedra podría haber sido utilizada para registrar información espacial o temporal, lo que invita a futuras comparaciones con datos astronómicos y otros artefactos arqueológicos.

## Referencias

- **Transformada de Fourier:** Proceso matemático para analizar la frecuencia de señales (ver: Bracewell, R. N. *The Fourier Transform and Its Applications*).
- **PCA:** Jolliffe, I. *Principal Component Analysis*.
- **t-SNE:** van der Maaten, L., & Hinton, G. *Visualizing Data using t-SNE*.
- **Fuzzy C-means:** Bezdek, J. C. *Pattern Recognition with Fuzzy Objective Function Algorithms*.
