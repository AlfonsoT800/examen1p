**Informe: Aplicación de Big Data al sistema de sensores industriales**

Nombre: MALTRANA LUNA ELIAS FRANCISCO

Grupo: IDIA 222

**5. Las 5 V aplicadas al proyecto**

| V | Relación con el sistema de sensores | Ejemplo concreto | CSV actual o ampliación futura |
|---|---|---|---|
| Volumen | Cantidad de datos que producen los sensores | El CSV tiene 100,000 registros de 40 sensores; con miles de sensores y una lectura por minuto se generarían millones de filas por día | CSV actual: 100,000 registros. Ampliación: miles de sensores |
| Velocidad | Rapidez con la que llegan y deben procesarse los datos | Cada sensor registra una lectura por minuto (en el CSV el intervalo mediano entre lecturas de un mismo sensor es de 1.00 minutos); en el futuro serían lecturas cada segundo | CSV actual: lecturas por minuto, guardadas en un archivo y no recibidas en tiempo real. Ampliación: una lectura por segundo |
| Variedad | Diferentes formatos de datos que deberá manejar el sistema | Hoy solo hay una tabla con seis columnas; después se sumarán fotografías de máquinas y reportes de mantenimiento | CSV actual: solo datos tabulares estructurados. Ampliación: fotografías, texto libre y mensajes JSON |
| Veracidad | Calidad y confiabilidad de los datos | No se encontraron nulos, identificadores duplicados ni vibraciones negativas; aun así los datos son simulados, por lo que no representan máquinas reales. Temperatura mínima observada: 45.0 °C; máxima: 104.99 °C | CSV actual: lo verificado en la calidad de datos. Ampliación: sensores reales con ruido, fallas de calibración y pérdidas de señal |
| Valor | Utilidad de los datos para tomar decisiones | Detectar alertas y priorizar mantenimiento: hay 6,954 lecturas sobre 85 °C y la(s) planta(s) Planta_3 concentra(n) más alertas (1777) | CSV actual: alertas y conteos por planta. Ampliación: predicción de fallas con historial de mantenimiento |

**6. Tipos de datos y procesamiento tradicional**

| Elemento | Clasificación | Justificación |
|---|---|---|
| CSV de sensores | Estructurado | Filas y columnas con esquema fijo |
| Mensaje JSON de un sensor | Semiestructurado | Tiene etiquetas y campos, pero el esquema es flexible |
| Fotografía de una máquina | No estructurado | Es una imagen sin esquema tabular |
| Texto libre de un reporte de mantenimiento | No estructurado | Es lenguaje natural sin estructura definida |

**Por qué 100,000 registros no son automáticamente Big Data:** el archivo cabe en la memoria de una computadora personal y analisis.py lo procesa en segundos con un solo programa y una sola máquina. Big Data no depende solo del número de filas, sino de que volumen, velocidad y variedad superen lo que las herramientas tradicionales pueden manejar. Este conjunto es tabular, estático, pequeño y de un solo formato.

**Limitaciones al aumentar la escala:** con miles de sensores y lecturas por segundo el volumen ya no cabría en la memoria de un equipo; la lectura completa del archivo sería lenta; una sola máquina sería un cuello de botella y un punto único de falla; un CSV no puede almacenar fotografías ni texto libre; y haría falta procesamiento distribuido y almacenamiento escalable.

**7. Batch y Streaming**

- **Tipo de procesamiento que realicé:** procesamiento por lotes (batch). El archivo ya estaba guardado y completo, y analisis.py lo leyó de una sola vez para calcular todos los resultados, sin depender de que los resultados estén listos en un tiempo límite.
- **Alerta pocos segundos después de una lectura mayor que 85 °C:** usaría streaming. Cada lectura debe evaluarse en cuanto llega; si se espera a juntar un lote, la alerta llegaría tarde y perdería utilidad.
- **Resumen al terminar el día:** usaría batch. Basta procesar las lecturas del día completo una vez, y nadie necesita ese resumen en segundos.
- **Relación con el tiempo:** la latencia que necesita el negocio decide el enfoque. Si el resultado se necesita en segundos, se requiere streaming; si puede esperar horas, batch es más simple y barato.

**8. Lambda y Kappa**

**Escenario A: Arquitectura Lambda**

Se pide combinar una ruta que recalcule el historial por lotes con otra que procese rápidamente las mediciones recientes. Eso es exactamente Lambda: una capa batch (historial completo y exacto), una capa de velocidad (lo reciente con baja latencia) y una capa de servicio que une ambos resultados.

```
                       +--> [Capa Batch: recalcula historial] ----+
 Sensores --> [Ingesta] |                                          +--> [Capa de Servicio] --> Consultas
                        +--> [Capa Speed: mediciones recientes] ---+
```

**Escenario B: Arquitectura Kappa**

Se pide una sola lógica de procesamiento de eventos y conservar las mediciones para reprocesarlas cuando sea necesario. Kappa usa un único flujo de streaming sobre un registro inmutable de eventos; si cambia la lógica, se reprocesa desde ese registro sin mantener dos códigos.

```
Sensores --> [Log de eventos inmutable] --> [Motor de streaming: única lógica] --> [Almacén / Consultas]
                       ^                                   |
                       +------- reprocesar desde el log ---+
```

**9. Analítica descriptiva, predictiva y prescriptiva**

**Descriptiva (hallazgos reales del análisis):**

1. Se registraron 6,954 lecturas con temperatura mayor que 85 °C, el 6.95% de las 100,000 mediciones. La(s) planta(s) con más alertas es/son Planta_3 con 1777 alertas.
2. La temperatura máxima fue 104.99 °C, registrada en: sensor S023 el 01/09/26 22:23 (planta Planta_3); sensor S019 el 02/09/26 13:11 (planta Planta_2); sensor S014 el 02/09/26 15:23 (planta Planta_2); sensor S030 el 02/09/26 16:02 (planta Planta_3). La(s) planta(s) con mayor temperatura promedio es/son Planta_3 con 66.77 °C.

**Predictiva:**

- Pregunta: ¿qué sensores o máquinas, como S027 (con 211 alertas cada uno en el CSV), tienen mayor probabilidad de superar 85 °C en los próximos días?
- Datos adicionales necesarios: historial de fallas y paros reales, bitácora de mantenimiento, carga de trabajo de cada máquina, temperatura ambiente, edad del equipo y más tiempo de mediciones para ver tendencias. En este CSV la correlación entre temperatura y vibración es 0.001, con vibración promedio de 3.022 mm/s en alertas frente a 3.002 mm/s sin alerta, y eso por sí solo no basta para predecir fallas.

**Prescriptiva:**

- Acción propuesta: ante un riesgo previsto de sobrecalentamiento, programar una inspección anticipada de las máquinas con alertas recurrentes (empezando por la planta Planta_3) en lugar de esperar a que fallen.
- Información a revisar antes de decidir: si las alertas son recurrentes o aisladas, la vibración de la misma máquina, su historial de mantenimiento, el costo de detener la producción, y si el sensor está bien calibrado.

*Una lectura sobre 85 °C es una alerta del ejercicio; por sí sola no demuestra que una máquina vaya a fallar.*
