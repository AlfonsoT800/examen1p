"""Análisis de sensores industriales (datos simulados).

Ejecutar desde la carpeta del proyecto:
    python analisis.py
"""
from pathlib import Path

import pandas as pd

# ---------- Rutas relativas a este archivo ----------
BASE = Path(__file__).parent
RUTA_CSV = BASE / "data" / "sensores_industriales.csv"
RUTA_ALERTAS = BASE / "resultados" / "alertas.csv"

UMBRAL = 85  # °C, regla didáctica del examen

# ---------- 1. Leer el archivo ----------
df = pd.read_csv(RUTA_CSV)

# ---------- 2. Registros y sensores distintos ----------
print("=== 1. Registros y sensores ===")
print(f"Cantidad de registros: {len(df):,}")
print(f"Sensores distintos: {df['id_sensor'].nunique()}")

# ---------- 3. Temperatura promedio por planta ----------
print("\n=== 2. Temperatura promedio por planta (°C) ===")
promedios = df.groupby("planta")["temperatura_c"].mean().round(2)
print(promedios.to_string())

# ---------- 4. Temperatura máxima (con empates) ----------
print("\n=== 3. Temperatura máxima ===")
t_max = df["temperatura_c"].max()
filas_max = df[df["temperatura_c"] == t_max]
print(f"Temperatura máxima: {t_max} °C ({len(filas_max)} lectura(s) con ese valor)")
print(filas_max[["id_registro", "id_sensor", "planta", "fecha_hora", "temperatura_c"]]
      .to_string(index=False))

# ---------- 5. Lecturas con alerta ----------
alertas = df[df["temperatura_c"] > UMBRAL]
print(f"\n=== 4. Lecturas con temperatura > {UMBRAL} °C ===")
print(f"Total de alertas: {len(alertas):,}")

# ---------- 6. Planta con más alertas (con empates) ----------
print("\n=== 5. Planta con más alertas ===")
alertas_por_planta = alertas["planta"].value_counts()
print(alertas_por_planta.to_string())
maximo = alertas_por_planta.max()
ganadoras = alertas_por_planta[alertas_por_planta == maximo].index.tolist()
print(f"Planta(s) con más alertas: {', '.join(ganadoras)} ({maximo:,} alertas)")

# ---------- 7. Exportar alertas ----------
RUTA_ALERTAS.parent.mkdir(exist_ok=True)  # crea resultados/ si no existe
alertas.to_csv(RUTA_ALERTAS, index=False)
print(f"\n=== 6. Exportación ===")
print(f"Se guardaron {len(alertas):,} alertas en {RUTA_ALERTAS.relative_to(BASE)}")
