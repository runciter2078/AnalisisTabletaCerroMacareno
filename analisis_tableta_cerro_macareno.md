# Análisis estadístico y de Inteligencia Artificial de la Tableta de Cerro Macareno

**Autor:** Pablo Beret Grande (abril 2025)  

---

## Resumen

Este estudio analiza la Tableta de Cerro Macareno mediante técnicas estadísticas e inteligencia artificial. Se transcribieron las marcas de la tablilla, originalmente codificadas en múltiples estados, y se simplificaron a un modelo que conserva tres estados: **vertical**, **horizontal** y **vacío**. Se aplicaron métodos de autocorrelación espacial, transformada de Fourier (FFT), reducción de dimensionalidad (PCA y t-SNE) y clustering difuso (Fuzzy C-means) para explorar la estructura subyacente y evaluar la influencia de la orientación de lectura (horizontal vs. vertical).

**Palabras clave:** Tableta de Cerro Macareno, análisis estadístico, inteligencia artificial, autocorrelación espacial, FFT, PCA, t-SNE, clustering difuso, arqueología, patrones astronómicos.

---

## Abstract

This study analyzes the Tableta de Cerro Macareno using statistical and artificial intelligence techniques. The tablet markings, originally encoded in multiple states, are simplified to a model that preserves three states: vertical, horizontal, and blank. Spatial autocorrelation, Fourier transform (FFT), dimensionality reduction (PCA and t-SNE), and fuzzy clustering (Fuzzy C-means) methods are applied to explore the underlying structure and assess the impact of reading orientation (horizontal vs. vertical).

**Key Words:** Tableta de Cerro Macareno, statistical analysis, artificial intelligence, spatial autocorrelation, FFT, PCA, t-SNE, fuzzy clustering, archaeology, astronomical patterns.

---

## Introducción

La Tableta de Cerro Macareno es un artefacto arqueológico cuya función y significado han generado múltiples hipótesis. En este estudio se transcribieron las marcas de la tablilla, inicialmente codificadas en varios estados (vertical, horizontal, inclinaciones a la derecha e izquierda, etc.), y se aplicaron técnicas estadísticas e inteligencia artificial para determinar la estructura subyacente. Los análisis preliminares revelaron que, para fines prácticos, el sistema se comporta de forma binaria (vertical vs. horizontal), manteniéndose un tercer estado para las casillas en blanco.  

Con el fin de investigar si la orientación de lectura (horizontal o vertical) afecta a la interpretación, se llevaron a cabo los mismos análisis en dos versiones de la matriz de datos: la original (asumida como "horizontal") y su traspuesta (denominada "vertical"). A continuación, se describen los métodos empleados y los resultados obtenidos, incluyendo las conclusiones derivadas de ambos enfoques.

---

## Historia y Contexto

La Tableta fue hallada en el yacimiento del Cerro Macareno, en la provincia de Sevilla, y ha suscitado diversas interpretaciones: desde un registro de sucesos hasta un proto-sistema de escritura. Ante la ausencia de un corpus comparativo amplio, este estudio se centra en analizar la distribución de las marcas para:

1. Verificar si la distribución sigue patrones no aleatorios.  
2. Determinar si la orientación de lectura influye en la estructura detectada.  
3. Explorar posibles correlaciones con patrones astronómicos o registros de fenómenos temporales.

---

## Metodología

### 1. Transcripción y Codificación de Datos

Inicialmente se identificaron múltiples categorías en las marcas (1, 1.5, 2, 3, 3.5, 4 y 5). Para el análisis se simplificó el sistema a un modelo de tres estados:

- **1:** Trazos "verticales" (valores originales menores a 2.5, excluyendo los vacíos).  
- **3:** Trazos "horizontales" (valores originales mayores o iguales a 2.5, excluyendo los vacíos).  
- **5:** Casillas en blanco o vacías.

A continuación se muestra un ejemplo del DataFrame original (orientación horizontal) antes de la transformación:

![DataFrame original (orientación horizontal)](/data/dataframe_original_horizontal.png)

### 2. Análisis Estadísticos y de IA Aplicados

#### 2.1 Autocorrelación Espacial

Se evaluó la estructura espacial calculando:

- **Sumas por filas y columnas:** Permiten detectar concentraciones de trazos verticales u horizontales.
- **Promedio de vecinos (vecindad de Moore):** Para cada celda se calcula el promedio de sus 8 vecinos en una vecindad 3×3.
- **Coeficiente de correlación de Pearson:**  
  \[
  r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}
  \]
  donde \(x_i\) es el valor de la celda y \(y_i\) el promedio de sus vecinos. Un \(r\) moderado o alto indica que celdas con valores similares tienden a agruparse.

#### 2.2 Transformada de Fourier (FFT)

La FFT se aplicó a las sumas por filas y columnas para detectar periodicidades en la distribución. La transformada se define como:

\[
X(k)=\sum_{n=0}^{N-1}x(n)\,e^{-i\,2\pi\frac{k\,n}{N}}
\]

Esta técnica permite identificar posibles ciclos o patrones repetitivos, que en una hipótesis astronómica podrían relacionarse con fenómenos cíclicos.

#### 2.3 Reducción de Dimensionalidad: PCA y t-SNE

- **PCA (Análisis de Componentes Principales):**  
  Se emplea para reducir la dimensionalidad del conjunto de datos y extraer las direcciones de mayor varianza.
  
- **t-SNE:**  
  Técnica no lineal que permite visualizar agrupamientos latentes en datos de alta dimensión. Se ajustaron parámetros (por ejemplo, el _perplexity_) para obtener visualizaciones coherentes, especialmente en muestras pequeñas.

#### 2.4 Clustering Difuso (Fuzzy C-means)

El algoritmo Fuzzy C-means permite que cada celda tenga un grado de pertenencia a cada clúster. El método minimiza la siguiente función objetivo:

\[
J_m=\sum_{i=1}^{N}\sum_{j=1}^{C}u_{ij}^m \, \|x_i-c_j\|^2
\]

donde:
- \(u_{ij}\) es el grado de pertenencia de la muestra \(x_i\) al clúster \(j\),
- \(c_j\) es el centro del clúster,
- \(m\) es el coeficiente de fuzzificación.

Se utiliza el Fuzzy Partition Coefficient (FPC) para evaluar la calidad de la partición, siendo valores cercanos a 1 indicativos de una partición nítida.

#### 2.5 Orientación Horizontal vs. Orientación Vertical

Para evaluar si la orientación de lectura altera los resultados, se repitieron los análisis en:
- **Orientación Horizontal:** Matriz en su forma original.  
- **Orientación Vertical:** Matriz traspuesta (lo que equivale a "rotar" la tablilla 90º).

Se mantuvieron los mismos códigos (1 para "vertical", 3 para "horizontal" y 5 para "vacío") para facilitar la comparación.

---

## Resultados

### 3.1 Orientación Horizontal

1. **Estadísticas Descriptivas (excluyendo vacíos):**  
   - Media: ~2.39  
   - Mediana: 3.00  
   - Desviación estándar: ~1.10  
   
   Estos valores, junto con el histograma de frecuencias, sugieren dos agrupaciones (valores próximos a 1 y valores cercanos a 3).

2. **Autocorrelación y FFT:**  
   - Se detectan diferencias en las sumas por filas y columnas, lo que indica bloques diferenciados.  
   - La FFT no muestra picos de periodicidad astronómica claramente definidos, pero revela patrones de distribución.
   
   ![Espectro FFT de filas (Horizontal)](/data/fft_filas_horizontal.png)
   ![Espectro FFT de columnas (Horizontal)](/data/fft_columnas_horizontal.png)

3. **Reducción de Dimensionalidad (PCA y t-SNE):**  
   - **PCA (Horizontal):** Muestra cierta dispersión con indicios de dos agrupaciones, aunque no tan definidas.  
   - **t-SNE (Horizontal):** Evidencia grupos más claros, con algunos puntos intermedios.
   
   ![PCA de la tabla (Horizontal)](/data/pca_horizontal.png)
   ![t-SNE de la tabla (Horizontal)](/data/tsne_horizontal.png)

4. **Clustering Difuso (Fuzzy C-means, k=2):**  
   - Se obtuvo un FPC de aproximadamente 0.65–0.70, lo que sugiere una partición robusta en dos clústeres.
   
   ![Clusters (Fuzzy C-means) para k=2 (Horizontal)](/data/fuzzy_horizontal.png)

**Conclusiones de la Orientación Horizontal:**  
Los datos se agrupan en dos bloques diferenciados (1 y 3) de forma consistente, validando la propuesta de un modelo "binario" (más el estado 5 para los vacíos). Aunque la FFT no muestra periodicidades astronómicas evidentes, la presencia de patrones espaciales y la robustez del clustering refuerzan la hipótesis de una estructura intencional.

---

### 3.2 Orientación Vertical

Para simular la lectura "vertical" de la tablilla se transpuso la matriz. Esto implica que las filas y columnas intercambian rol, lo que a veces invierte la interpretación de "vertical" y "horizontal", pero se mantienen los mismos códigos (1, 3 y 5).

1. **Estadísticas Descriptivas (excluyendo vacíos):**  
   Se observa que la distribución sigue mostrando dos modos, similar a la orientación horizontal.

2. **Autocorrelación y FFT (Vertical):**  
   - Se repiten los cálculos de sumas por filas y columnas y se aplica la FFT.  
   - Los resultados son similares: no se aprecian picos claros de periodicidad, pero se confirman patrones de distribución.
   
   ![Espectro FFT de filas (Vertical)](/data/fft_filas_vertical.png)
   ![Espectro FFT de columnas (Vertical)](/data/fft_columnas_vertical.png)

3. **Reducción de Dimensionalidad (PCA y t-SNE):**  
   - **PCA (Vertical):** Muestra dos tendencias, aunque la separación puede variar según la varianza acumulada.
   - **t-SNE (Vertical):** En algunos casos se observa una agrupación casi perfecta en dos bloques, lo que podría sugerir que la lectura vertical (o la transposición) resalta de forma más clara la segmentación.
   
   ![PCA de la tabla (Vertical)](/data/pca_vertical.png)
   ![t-SNE de la tabla (Vertical)](/data/tsne_vertical.png)

4. **Clustering Difuso (Fuzzy C-means, k=2):**  
   - El FPC (~0.65) es similar al obtenido en orientación horizontal, confirmando una partición robusta en dos grupos.
   
   ![Clusters (Fuzzy C-means) para k=2 (Vertical)](/data/fuzzy_vertical.png)

**Conclusiones de la Orientación Vertical:**  
Los análisis confirman la persistencia de una estructura bimodal incluso al transponer la matriz. La agrupación casi perfecta en t-SNE en algunos ensayos podría sugerir que la lectura vertical revela una segmentación más clara, o bien, ofrece una visión complementaria a la orientación horizontal. En cualquier caso, los métodos indican que la organización interna de la tablilla es robusta y no depende de la dirección de lectura.

---

## Conclusiones Generales

1. **Validez del Modelo Trinario (1, 3, 5):**  
   La transformación a un modelo simplificado de tres estados (1 = vertical, 3 = horizontal, 5 = vacío) facilita el análisis y revela una estructura fundamentalmente bimodal.

2. **Orientación Horizontal vs. Vertical:**  
   - Ambos enfoques arrojan resultados coherentes: la tablilla presenta dos grupos claramente diferenciados.  
   - En la orientación vertical, algunas técnicas (como t‑SNE) muestran una separación más nítida, lo que podría indicar que la lectura vertical se ajusta mejor a la organización original o, al menos, ofrece una visión complementaria.

3. **Patrones Espaciales y FFT:**  
   - Aunque no se detectaron periodicidades astronómicas claras, los picos moderados en la FFT y el análisis de autocorrelación evidencian que la distribución de trazos no es aleatoria.
   - El coeficiente de correlación de Pearson y las sumas por filas y columnas refuerzan la existencia de bloques diferenciados.

4. **Reducción de Dimensionalidad (PCA y t-SNE):**  
   - La PCA sugiere la existencia de dos direcciones principales de variabilidad.  
   - El t-SNE evidencia de forma más clara la división en dos grupos, especialmente en la orientación vertical en ciertos ensayos.

5. **Clustering Difuso (Fuzzy C-means):**  
   - Con \( k=2 \), se obtiene un FPC cercano a 0.65–0.70, indicando una partición estable en dos clústeres.  
   - Este hallazgo se mantiene en ambas orientaciones, reforzando la hipótesis de una estructura bimodal.

**Perspectivas Futuras:**  
- Integrar información contextual adicional (por ejemplo, correlaciones con ciclos lunares o solares) para evaluar si la disposición de las marcas responde a motivos astronómicos.  
- Explorar metodologías avanzadas (como redes neuronales convolucionales) que consideren la distribución espacial completa.  
- Investigar la posibilidad de más de dos estados relevantes en función de características adicionales de las marcas.

---

## Referencias

- **Bracewell, R. N.** *The Fourier Transform and Its Applications*. McGraw-Hill.  
- **Jolliffe, I.** *Principal Component Analysis*. Springer.  
- **van der Maaten, L., & Hinton, G.** (2008). *Visualizing Data using t-SNE*. Journal of Machine Learning Research, 9.  
- **Bezdek, J. C.** *Pattern Recognition with Fuzzy Objective Function Algorithms*. Springer.  

---
