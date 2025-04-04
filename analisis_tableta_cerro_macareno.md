# Análisis estadístico y de Inteligencia Artificial de la Tableta de Cerro Macareno

**Autor:** Pablo Beret Grande (abril 2025)  

---

## Resumen

Este estudio analiza la Tableta de Cerro Macareno mediante técnicas estadísticas e inteligencia artificial. Se transcribieron las marcas de la tablilla, originalmente codificadas en múltiples estados, y se simplificaron a un modelo que conserva tres estados: vertical, horizontal y vacío. Se aplicaron métodos de autocorrelación espacial, transformada de Fourier (FFT), reducción de dimensionalidad (PCA y t-SNE) y clustering difuso (Fuzzy C-means) para explorar la estructura subyacente y evaluar la influencia de la orientación de lectura (horizontal vs. vertical).  

**Palabras clave:** Tableta de Cerro Macareno, análisis estadístico, inteligencia artificial, autocorrelación espacial, FFT, PCA, t-SNE, clustering difuso, arqueología, patrones astronómicos.

---

## Abstract

This study analyzes the Tableta de Cerro Macareno using statistical and artificial intelligence techniques. The tablet markings, originally encoded in multiple states, are simplified to a model that preserves three states: vertical, horizontal, and blank. Spatial autocorrelation, Fourier transform (FFT), dimensionality reduction (PCA and t-SNE), and fuzzy clustering (Fuzzy C-means) methods are applied to explore the underlying structure and assess the impact of reading orientation (horizontal vs. vertical).

**Key Words:** Tableta de Cerro Macareno, statistical analysis, artificial intelligence, spatial autocorrelation, FFT, PCA, t-SNE, fuzzy clustering, archaeology, astronomical patterns.

---

## Introducción

La Tableta de Cerro Macareno es un artefacto arqueológico cuya función y significado han generado múltiples hipótesis. En este estudio, se transcribieron las marcas de la tablilla, inicialmente codificadas en varios estados (vertical, horizontal, inclinaciones a la derecha e izquierda, etc.), y se aplicaron técnicas estadísticas e inteligencia artificial para determinar la estructura subyacente. A partir de análisis preliminares, se observó que las marcas pueden agruparse de manera fundamental en dos grandes categorías (vertical vs. horizontal), manteniendo un tercer estado para las casillas en blanco.  

Con el fin de investigar si la orientación de lectura (horizontal o vertical) afecta a la interpretación, se llevaron a cabo los mismos análisis en dos versiones de la matriz de datos: la original (asumida como “horizontal”) y su traspuesta (denominada “vertical”). A continuación, se describen los métodos empleados y los resultados obtenidos, incluyendo las conclusiones derivadas de ambos enfoques.

---

## Historia y Contexto

La Tableta fue hallada en el yacimiento del Cerro Macareno, en la provincia de Sevilla. Diversas interpretaciones han sugerido que podría tratarse de un registro de sucesos, un inventario o incluso un proto-sistema de escritura. Dada la falta de un corpus comparativo amplio, en este trabajo se recurre a métodos estadísticos y de inteligencia artificial para:

1. Verificar si la distribución de las marcas sigue patrones no aleatorios.  
2. Determinar si la orientación de lectura influye en la estructura detectada.  
3. Explorar la posibilidad de que existan correlaciones con patrones astronómicos o con registros de fenómenos temporales.

---

## Metodología

### 1. Transcripción y Codificación de Datos

Inicialmente se identificaron múltiples categorías en las marcas (1, 1.5, 2, 3, 3.5, 4 y 5). Para fines de análisis, se simplificó a un modelo con tres estados:

- **1:** Trazos “verticales” (valores originales < 2.5, excluyendo los vacíos).  
- **3:** Trazos “horizontales” (valores originales ≥ 2.5, excluyendo los vacíos).  
- **5:** Casillas en blanco o vacías.

En la siguiente imagen se muestra un ejemplo del DataFrame original (orientación horizontal) antes de la conversión a modelo binario:

- **Archivo a guardar en `/data`:**  
  `dataframe_original_horizontal.png`  
  (Imagen que represente el DataFrame tal como se visualiza en la transcripción original.)

```plaintext
![DataFrame original (orientación horizontal)](/data/dataframe_original_horizontal.png)
```

### 2. Análisis Estadísticos y de IA Aplicados

A continuación se describen los principales métodos empleados tanto para la orientación horizontal como para la vertical (matriz traspuesta).

#### 2.1 Autocorrelación Espacial

- **Sumas por filas y columnas:** Se calculan para detectar si existen concentraciones de trazos verticales u horizontales.  
- **Promedio de vecinos (vecindad de Moore):** Para cada celda se calcula el promedio de sus 8 vecinos (en un entorno de 3×3).  
- **Coeficiente de correlación de Pearson** entre el valor de la celda y el promedio de sus vecinos. Valores positivos moderados o altos indican que celdas con un mismo estado tienden a agruparse espacialmente.

#### 2.2 Transformada de Fourier (FFT)

Se aplica la FFT a las sumas por filas y columnas con el fin de buscar periodicidades. Una periodicidad marcada podría sugerir patrones cíclicos o repetitivos (potencialmente asociados a hipótesis astronómicas). La fórmula base de la FFT es:

\[
X(k)=\sum_{n=0}^{N-1}x(n)\,e^{-i\,2\pi\frac{k\,n}{N}}
\]

#### 2.3 Reducción de Dimensionalidad: PCA y t-SNE

- **PCA (Análisis de Componentes Principales):** Identifica direcciones de mayor varianza en el espacio de datos.  
- **t-SNE:** Proyección no lineal que agrupa muestras similares en el espacio de visualización, facilitando la detección de clústeres latentes.

En ambos casos, se crean matrices donde cada fila representa una unidad de observación (p. ej., fila o columna de la tablilla, o cada celda con sus características), y se reduce la dimensionalidad para visualizar si emergen grupos diferenciados.

#### 2.4 Clustering Difuso (Fuzzy C-means)

El algoritmo Fuzzy C-means asigna a cada muestra un grado de pertenencia a cada clúster, minimizando:

\[
J_m=\sum_{i=1}^{N}\sum_{j=1}^{C}u_{ij}^m \, \|x_i-c_j\|^2
\]

donde:
- \(u_{ij}\) es el grado de pertenencia de la muestra \(x_i\) al clúster \(j\).  
- \(c_j\) es el centro del clúster.  
- \(m\) es el coeficiente de fuzzificación.

Se evalúa la partición con el Fuzzy Partition Coefficient (FPC). Un valor cercano a 1 indica una partición más “nítida”.

#### 2.5 Orientación Horizontal vs. Orientación Vertical

Para evaluar si la forma de lectura altera los resultados, se repiten los análisis anteriores en:

- **Orientación Horizontal:** Matriz tal como se transcribió originalmente.  
- **Orientación Vertical:** Matriz traspuesta (equivalente a “rotar” la tablilla 90º).  

Esto permite comparar si la estructura subyacente (bimodalidad, agrupamientos, periodicidades, etc.) se mantiene o varía.

---

## 3. Resultados

### 3.1 Orientación Horizontal

1. **Estadísticas Descriptivas (excluyendo vacíos):**  
   - Media: ~2.39  
   - Mediana: 3.00  
   - Desviación estándar: ~1.10  

   Estos valores, junto con el histograma de frecuencias, sugieren dos agrupaciones (valores próximos a 1 y valores cercanos a 3).

2. **Autocorrelación y FFT:**  
   - Se observan diferencias en las sumas por filas y columnas.  
   - La FFT no muestra picos de periodicidad astronómica claros, pero sí ciertos máximos que indican organización no aleatoria.

   - **Archivos recomendados en `/data`:**  
     - `fft_filas_horizontal.png`  
     - `fft_columnas_horizontal.png`

   ```plaintext
   ![Espectro FFT de filas (Horizontal)](/data/fft_filas_horizontal.png)
   ![Espectro FFT de columnas (Horizontal)](/data/fft_columnas_horizontal.png)
   ```

3. **Reducción de Dimensionalidad (PCA y t-SNE):**  
   - **PCA (Horizontal):** Muestra cierta dispersión, con indicios de dos agrupaciones, aunque no tan definidas.  
   - **t-SNE (Horizontal):** Visualiza grupos más claros, pero con algunos puntos intermedios.

   - **Archivos recomendados en `/data`:**  
     - `pca_horizontal.png`  
     - `tsne_horizontal.png`

   ```plaintext
   ![PCA de la tabla (Horizontal)](/data/pca_horizontal.png)
   ![t-SNE de la tabla (Horizontal)](/data/tsne_horizontal.png)
   ```

4. **Clustering Difuso (Fuzzy C-means, k=2):**  
   - FPC ≈ 0.65–0.70, lo cual sugiere una partición robusta en dos clusters.  
   - El mapa de calor de la pertenencia difusa evidencia un patrón bimodal.

   - **Archivo recomendado en `/data`:**  
     - `fuzzy_horizontal.png`

   ```plaintext
   ![Clusters (Fuzzy C-means) para k=2 (Horizontal)](/data/fuzzy_horizontal.png)
   ```

**Conclusiones de la Orientación Horizontal:**  
Los datos se agrupan en dos bloques diferenciados (1 y 3) de forma consistente, validando la propuesta de un modelo “binario” (más el estado 5 para los vacíos). Aunque la FFT no muestra periodicidades astronómicas evidentes, la presencia de patrones espaciales y la robustez del clustering refuerzan la hipótesis de una estructura intencional.

---

### 3.2 Orientación Vertical

Para simular la lectura “vertical” de la tablilla, se transpuso la matriz. Esto conlleva que las filas y columnas intercambien su rol, lo que a veces invierte la interpretación de “vertical” y “horizontal” en los trazos. Sin embargo, se mantuvieron los mismos códigos (1 para “vertical”, 3 para “horizontal” y 5 para “vacío”) tras la transposición, con el fin de comparar la estructura puramente numérica.

1. **Estadísticas Descriptivas (excluyendo vacíos):**  
   - Se mantiene la misma escala de valores (1 y 3), por lo que la media y mediana continúan reflejando dos grupos principales.  
   - Al igual que en la orientación horizontal, se observan dos modos en la distribución.

2. **Autocorrelación y FFT (Vertical):**  
   - Se repiten los mismos cálculos de sumas por filas y columnas, y se aplica la FFT.  
   - Los resultados son similares: no aparecen picos claros de periodicidad astronómica, pero sí patrones de distribución.  

   - **Archivos recomendados en `/data`:**  
     - `fft_filas_vertical.png`  
     - `fft_columnas_vertical.png`

   ```plaintext
   ![Espectro FFT de filas (Vertical)](/data/fft_filas_vertical.png)
   ![Espectro FFT de columnas (Vertical)](/data/fft_columnas_vertical.png)
   ```

3. **Reducción de Dimensionalidad (PCA y t-SNE):**  
   - **PCA (Vertical):** También muestra dos tendencias, aunque la separación puede ser menos o más marcada dependiendo de la escala y la varianza acumulada.  
   - **t-SNE (Vertical):** En algunos casos, se ha observado una agrupación casi perfecta en dos bloques, lo que podría indicar que la lectura vertical (o la transposición) revela una segmentación más clara.

   - **Archivos recomendados en `/data`:**  
     - `pca_vertical.png`  
     - `tsne_vertical.png`

   ```plaintext
   ![PCA de la tabla (Vertical)](/data/pca_vertical.png)
   ![t-SNE de la tabla (Vertical)](/data/tsne_vertical.png)
   ```

4. **Clustering Difuso (Fuzzy C-means, k=2):**  
   - El FPC obtenido (~0.65) es muy similar al de la orientación horizontal, indicando una partición igualmente válida en dos grupos.  
   - El mapa de calor resultante sugiere que la distribución sigue un patrón similar al horizontal, aunque “girado”.

   - **Archivo recomendado en `/data`:**  
     - `fuzzy_vertical.png`

   ```plaintext
   ![Clusters (Fuzzy C-means) para k=2 (Vertical)](/data/fuzzy_vertical.png)
   ```

**Conclusiones de la Orientación Vertical:**  
Los análisis confirman la persistencia de una estructura bimodal, incluso al transponer la matriz. La perfecta agrupación en t-SNE en algunos ensayos podría sugerir que la “verdadera” orientación de lectura es vertical o, al menos, que esta visión refuerza la separación en dos bloques. Sin embargo, no se puede concluir de manera definitiva solo con estos métodos. El hecho de que el clustering difuso y las estadísticas descriptivas muestren resultados análogos indica que la tablilla conserva su organización interna independientemente de la orientación, lo que a su vez puede interpretarse como evidencia de una disposición intencional robusta.

---

## 4. Conclusiones Generales

1. **Validez del Modelo Trinario (1, 3, 5):**  
   La transformación a un modelo simplificado de tres estados (1 = vertical, 3 = horizontal, 5 = vacío) facilita el análisis y revela una estructura fundamentalmente bimodal.  

2. **Orientación Horizontal vs. Vertical:**  
   - Ambos enfoques arrojan resultados coherentes: la tablilla presenta dos grupos claramente diferenciados.  
   - En la orientación vertical, algunas técnicas (como t-SNE) muestran una separación más nítida, lo que podría indicar que la lectura vertical se ajusta mejor a la organización original de la tablilla o, al menos, ofrece una visión complementaria.

3. **Patrones Espaciales y FFT:**  
   - Aunque no se detectaron periodicidades astronómicas claras, la existencia de picos moderados en la FFT y de correlaciones espaciales indica que la distribución de trazos no es aleatoria.  
   - El coeficiente de correlación de Pearson entre celdas y sus vecinos, junto con las sumas por filas y columnas, refuerza la idea de que las marcas están organizadas en bloques.

4. **Reducción de Dimensionalidad (PCA y t-SNE):**  
   - En ambos modos de orientación, la PCA sugiere la existencia de dos grandes direcciones de variabilidad.  
   - El t-SNE, más sensible a distancias locales, evidencia con mayor claridad la división en dos grupos, especialmente en la orientación vertical en algunos ensayos.

5. **Clustering Difuso (Fuzzy C-means):**  
   - Con \( k=2 \), se obtiene un FPC cercano a 0.65–0.70, señal de una partición estable en dos clústeres.  
   - Este hallazgo se mantiene tanto en horizontal como en vertical, reforzando la hipótesis de una estructura bimodal.

**Perspectivas Futuras:**  
- Incorporar información contextual adicional (por ejemplo, correlaciones con ciclos lunares o solares) podría ayudar a determinar si la disposición de las marcas responde a motivos astronómicos.  
- Explorar metodologías de segmentación y clasificación más avanzadas (p. ej., redes neuronales convolucionales) que consideren la distribución espacial completa, no solo las sumas por filas o columnas.  
- Investigar la posibilidad de más de dos estados relevantes (además de los vacíos) en función de inclinaciones u otras características de las marcas.

---

## Referencias

- **Bracewell, R. N.** *The Fourier Transform and Its Applications*. McGraw-Hill.  
- **Jolliffe, I.** *Principal Component Analysis*. Springer.  
- **van der Maaten, L., & Hinton, G.** (2008). *Visualizing Data using t-SNE*. Journal of Machine Learning Research, 9.  
- **Bezdek, J. C.** *Pattern Recognition with Fuzzy Objective Function Algorithms*. Springer.  

---
