# Análisis estadístico y con métodos de inteligencia artificial de la Tableta de Cerro Macareno

**Autor:** Pablo Beret Grande (abril 2025)  

---

![Tableta Cerro Macareno](/data/tablilla.jpg)

## Resumen

Este estudio analiza la Tableta de Cerro Macareno mediante técnicas estadísticas e inteligencia artificial. Se transcribieron las marcas de la tablilla, originalmente codificadas en múltiples estados, y se simplificaron a un modelo que conserva tres estados: **vertical**, **horizontal** y **vacío**. Se aplicaron métodos de autocorrelación espacial, transformada de Fourier (FFT), reducción de dimensionalidad (PCA y t-SNE) y clustering difuso (Fuzzy C-means) para explorar la estructura subyacente y evaluar la influencia de la orientación de lectura (horizontal vs. vertical).

**Palabras clave:** Tableta de Cerro Macareno, análisis estadístico, inteligencia artificial, autocorrelación espacial, FFT, PCA, t-SNE, clustering difuso, arqueología, patrones astronómicos.

---

## Abstract

This study analyzes the Tableta de Cerro Macareno using statistical and artificial intelligence techniques. The tablet markings, originally encoded in multiple states, are simplified to a model that preserves three states: vertical, horizontal, and blank. Spatial autocorrelation, Fourier transform (FFT), dimensionality reduction (PCA and t-SNE), and fuzzy clustering (Fuzzy C-means) methods are applied to explore the underlying structure and assess the impact of reading orientation (horizontal vs. vertical).

**Key Words:** Tableta de Cerro Macareno, statistical analysis, artificial intelligence, spatial autocorrelation, FFT, PCA, t-SNE, fuzzy clustering, archaeology, astronomical patterns.

---

![Símbolos en la Tableta Cerro Macareno](/data/tablilla_2.jpg)

## Introducción

La Tableta de Cerro Macareno es un artefacto arqueológico cuya función y significado han generado múltiples hipótesis. En este estudio se transcribieron las marcas de la tablilla, inicialmente codificadas en varios estados (vertical, horizontal, inclinaciones a la derecha e izquierda, etc.), y se aplicaron técnicas estadísticas e inteligencia artificial para determinar la estructura subyacente. Los análisis preliminares revelaron que, para fines prácticos, el sistema se comporta de forma binaria (vertical vs. horizontal), manteniéndose un tercer estado para las casillas en blanco.  

Con el fin de investigar si la orientación de lectura (horizontal o vertical) afecta a la interpretación, se llevaron a cabo los mismos análisis en dos versiones de la matriz de datos: la original (asumida como "horizontal") y su traspuesta (denominada "vertical"). A continuación, se describen los métodos empleados y los resultados obtenidos, incluyendo las conclusiones derivadas de ambos enfoques.

---

## Historia y contexto

La Tableta fue hallada en el yacimiento del Cerro Macareno, en la provincia de Sevilla, y ha suscitado diversas interpretaciones: desde un registro de sucesos hasta un proto-sistema de escritura. Ante la ausencia de un corpus comparativo amplio, este estudio se centra en analizar la distribución de las marcas para:

1. Verificar si la distribución sigue patrones no aleatorios.  
2. Determinar si la orientación de lectura influye en la estructura detectada.  
3. Explorar posibles correlaciones con patrones astronómicos o registros de fenómenos temporales.

---

## Metodología

### 1. Transcripción y codificación de datos

Inicialmente se identificaron múltiples categorías en las marcas (1, 1.5, 2, 3, 3.5, 4 y 5). Para el análisis se simplificó el sistema a un modelo de tres estados:

- **1:** Trazos "verticales" (valores originales menores a 2.5, excluyendo los vacíos).  
- **3:** Trazos "horizontales" (valores originales mayores o iguales a 2.5, excluyendo los vacíos).  
- **5:** Casillas en blanco o vacías.

A continuación se muestra un ejemplo del DataFrame original (orientación horizontal) antes de la transformación:

![DataFrame original (orientación horizontal)](/data/dataframe_original_horizontal.PNG)

### 2. Análisis estadísticos y de IA aplicados

#### 2.1 Autocorrelación espacial

Se evaluó la estructura espacial calculando:

- **Sumas por filas y columnas:** Permiten detectar concentraciones de trazos verticales u horizontales.
- **Promedio de vecinos (vecindad de Moore):** Para cada celda se calcula el promedio de sus 8 vecinos en una vecindad 3×3.
- **Coeficiente de correlación de Pearson:**  
  <img src="https://latex.codecogs.com/svg.image?r=\frac{\sum(x_i-\bar{x})(y_i-\bar{y})}{\sqrt{\sum(x_i-\bar{x})^2\sum(y_i-\bar{y})^2}}" alt="Coeficiente de correlación de Pearson" />

#### 2.2 Transformada de Fourier (FFT)

La FFT se aplicó a las sumas por filas y columnas para detectar periodicidades en la distribución. La transformada se define como:

<img src="https://latex.codecogs.com/svg.image?X(k)=\sum_{n=0}^{N-1}x(n)\,e^{-i\,2\pi\frac{k\,n}{N}}" alt="Transformada de Fourier (FFT)" />

#### 2.3 Reducción de dimensionalidad: PCA y t-SNE

- **PCA (Análisis de Componentes Principales):**  
  Se emplea para reducir la dimensionalidad del conjunto de datos y extraer las direcciones de mayor varianza. La transformación básica es:  
  <img src="https://latex.codecogs.com/svg.image?Z=XW" alt="Transformación PCA" />  
  donde \(W\) son los vectores propios de la matriz de covarianza de \(X\).

- **t-SNE:**  
  Técnica no lineal que permite visualizar agrupamientos latentes en datos de alta dimensión.

#### 2.4 Clustering difuso (Fuzzy C-means)

El algoritmo Fuzzy C-means minimiza la función objetivo:  
<img src="https://latex.codecogs.com/svg.image?J_m=\sum_{i=1}^{N}\sum_{j=1}^{C}u_{ij}^m\|x_i-c_j\|^2" alt="Función objetivo del Clustering Difuso (Fuzzy C-means)" />

donde \(u_{ij}\) es el grado de pertenencia de \(x_i\) al clúster \(j\), \(c_j\) es el centro del clúster, y \(m\) es el coeficiente de fuzzificación.

#### 2.5 Orientación horizontal vs. Orientación vertical

Para evaluar si la orientación de lectura altera los resultados, se repitieron los análisis en:
- **Orientación horizontal:** Matriz en su forma original.  
- **Orientación vertical:** Matriz traspuesta (equivalente a "rotar" la tablilla 90º).

---

## Resultados

### 3.1 Orientación horizontal

1. **Estadísticas descriptivas (excluyendo vacíos):**  
   - Media: ~2.39  
   - Mediana: 3.00  
   - Desviación estándar: ~1.10  

2. **Autocorrelación y FFT:**  
   ![Espectro FFT de filas (Horizontal)](/data/fft_filas_horizontal.PNG)
   ![Espectro FFT de columnas (Horizontal)](/data/fft_columnas_horizontal.PNG)

3. **Reducción de dimensionalidad:**  
   ![PCA de la tabla (Horizontal)](/data/pca_horizontal.PNG)
   ![t-SNE de la tabla (Horizontal)](/data/tsne_horizontal.PNG)

4. **Clustering difuso:**  
   ![Clusters (Fuzzy C-means) para k=2 (Horizontal)](/data/fuzzy_horizontal.PNG)

---

### 3.2 Orientación vertical

1. **FFT (Vertical):**  
   ![Espectro FFT de filas (Vertical)](/data/fft_filas_vertical.PNG)
   ![Espectro FFT de columnas (Vertical)](/data/fft_columnas_vertical.PNG)

2. **Reducción de dimensionalidad:**  
   ![PCA de la tabla (Vertical)](/data/pca_vertical.PNG)
   ![t-SNE de la tabla (Vertical)](/data/tsne_vertical.PNG)

3. **Clustering difuso:**  
   ![Clusters (Fuzzy C-means) para k=2 (Vertical)](/data/fuzzy_vertical.PNG)

---

## Conclusiones generales

Los análisis confirman una estructura bimodal robusta independiente de la orientación. Las técnicas de IA y estadística refuerzan la hipótesis de un registro no aleatorio, posiblemente vinculado a fenómenos espaciales o temporales.

---

## Referencias

- **Bracewell, R. N.** *The Fourier Transform and Its Applications*.  
- **Jolliffe, I.** *Principal Component Analysis*.  
- **van der Maaten, L., & Hinton, G.** *Visualizing Data using t-SNE*.  
- **Bezdek, J. C.** *Pattern Recognition with Fuzzy Objective Function Algorithms*.

---
