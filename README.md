# Análisis de sensores industriales

> **Aviso:** los datos de este proyecto son **simulados**.

## Objetivo

Analizar con Python las mediciones de temperatura y vibración de sensores instalados en cuatro plantas industriales: contar registros y sensores, calcular temperaturas promedio por planta, encontrar la temperatura máxima, detectar alertas (temperatura mayor que 85 °C; umbral didáctico del examen) y exportarlas a un archivo CSV.

## Descripción de los datos

Archivo: `data/sensores_industriales.csv` (100,000 mediciones simuladas, una lectura por sensor por minuto).

| Columna | Significado |
|---|---|
| `id_registro` | Identificador de la medición |
| `fecha_hora` | Fecha y hora de la lectura |
| `id_sensor` | Identificador del sensor |
| `planta` | Planta donde está instalado |
| `temperatura_c` | Temperatura en grados Celsius |
| `vibracion_mm_s` | Vibración en milímetros por segundo |

## Estructura del proyecto

```
data/sensores_industriales.csv   <- datos originales
analisis.py                      <- programa de análisis
analisis.ipynb                   <- mismo análisis, en notebook
resultados/alertas.csv           <- se genera al ejecutar
evidencias/                      <- captura de reproducibilidad
requirements.txt
```

## Instalación

Requiere Python 3.10 o superior. Desde la carpeta del proyecto:

**Windows (PowerShell):**
```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**macOS / Linux:**
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

Programa de Python:
```
python analisis.py
```

Notebook (opcional):
```
jupyter notebook analisis.ipynb
```
Luego usa **Run → Run All Cells**.

Al terminar se crea `resultados/alertas.csv` con todas las lecturas mayores que 85 °C y las mismas columnas del archivo original.
