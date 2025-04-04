# Análisis estadístico y de inteligencia artificial aplicado a la Tableta de Cerro Macareno

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Este repositorio contiene el análisis estadístico y de inteligencia artificial aplicado a la tableta de Cerro Macareno. Se utiliza un cuaderno Jupyter (`analisis.ipynb`) que integra técnicas de correlación espacial, transformada de Fourier (FFT), reducción de dimensionalidad (PCA y t-SNE) y clustering difuso (Fuzzy C-means) para explorar la organización de las marcas de la tablilla.

## Descripción

El estudio se basa en la transcripción de las marcas de la tableta, inicialmente codificadas en múltiples estados (vertical, horizontal, inclinaciones, etc.) y posteriormente simplificadas a un modelo binario (vertical vs. horizontal). Se analizan los datos en ambas orientaciones (horizontal y vertical) para evaluar la robustez de la estructura y la posibilidad de que la tableta registre información espacial o temporal, con hipótesis de origen arqueoastronómico.

## Estructura del Repositorio

- `analisis.ipynb`: Cuaderno Jupyter con el código completo del análisis.
- `analisis_tableta_cerro_macareno.md`: Documento con la metodología, teoría, resultados y conclusiones.
- `data/`: Carpeta que contiene imagenes y datos del proyecto.
- `requirements.txt`: Lista de dependencias necesarias (pandas, numpy, matplotlib, seaborn, scikit-learn, scikit-fuzzy, etc.).

## Uso

1. Clona el repositorio:
   ```bash
   git clone https://github.com/runciter2078/AnalisisTabletaCerroMacareno.git
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Abre el cuaderno Jupyter `analisis.ipynb` y ejecútalo para reproducir los análisis.

## Licencia

Este proyecto está bajo la licencia MIT. Para más detalles, consulta el archivo `LICENSE`.

## Contacto

Para cualquier consulta o sugerencia, por favor, abre un issue en el repositorio o contacta con Pablo Beret Grande.
```
