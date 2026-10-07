# Informe: aplicación al caso de Big Data

> Los datos del proyecto son **simulados**. Los resultados citados salen de ejecutar `analisis.py` sobre `data/sensores_industriales.csv`.

## Resultados del análisis que se usan en este informe

| Dato | Valor |
|---|---|
| Registros | 100,000 |
| Sensores distintos | 40 (10 por planta) |
| Periodo cubierto | del 01/09/26 0:00 al 02/09/26 17:39 (2,500 minutos) |
| Temperatura promedio por planta | Planta_1: 66.62 °C, Planta_2: 66.53 °C, Planta_3: 66.77 °C, Planta_4: 66.67 °C |
| Temperatura máxima | 104.99 °C (4 lecturas empatadas: S023, S019, S014 y S030) |
| Lecturas con temperatura > 85 °C | 6,954 (6.95 % del total) |
| Planta con más alertas | Planta_3, con 1,777 |
| Alertas por planta | Planta_3: 1,777, Planta_1: 1,737, Planta_4: 1,732, Planta_2: 1,708 |

---

## 5. Las 5 V aplicadas al proyecto

| V | Cómo se relaciona con el sistema de sensores | Ejemplo concreto | ¿Dónde aparece? |
|---|---|---|---|
| **Volumen** | Cantidad de datos que generan los sensores. Cada sensor produce una lectura por minuto y el total crece con cada sensor y cada día. | El CSV tiene 100,000 mediciones de 40 sensores. Con 1,000 sensores midiendo cada segundo se generarían 86,400,000 lecturas al día. | **CSV actual:** las 100,000 mediciones (un volumen pequeño, manejable en una computadora). **Ampliación:** los millones de lecturas por día. |
| **Velocidad** | Rapidez con la que llegan los datos y con la que hay que reaccionar a ellos. | Hoy llega una lectura por sensor por minuto. Con lecturas cada segundo, una temperatura de 104.99 °C debería detectarse en segundos y no al final del día. | **CSV actual:** solo se refleja la frecuencia de una lectura por minuto, pero el archivo ya está guardado y se analiza después. **Ampliación:** las mediciones cada segundo y la reacción en tiempo casi real. |
| **Variedad** | Diferentes formatos y tipos de datos que el sistema podría manejar. | El CSV tiene solo columnas numéricas y de texto. En el futuro se sumarían fotografías de las máquinas y reportes de mantenimiento en texto libre. | **CSV actual:** únicamente datos estructurados (una tabla). **Ampliación:** fotografías y reportes de mantenimiento (no estructurados). |
| **Veracidad** | Confianza en que los datos son correctos y completos. | En el CSV no hay valores vacíos ni registros con `id_registro` repetido, pero los datos son simulados, así que no se puede saber si un sensor real estuviera descalibrado y reportara 104.99 °C por error. | **CSV actual:** se pudo revisar que está completo y sin duplicados. **Ampliación:** con miles de sensores reales habría que detectar fallas de sensores, lecturas perdidas o datos atrasados. |
| **Valor** | Utilidad de los datos para tomar decisiones de negocio. | El análisis encontró 6,954 lecturas por encima de 85 °C y mostró que la Planta_3 tiene más alertas (1,777), lo que sirve para decidir dónde revisar primero las máquinas. | **CSV actual:** ya se obtiene este valor con el análisis. **Ampliación:** el valor crecería al detectar riesgos en tiempo real y combinar las lecturas con fotos y reportes. |

---

## 6. Tipos de datos y procesamiento tradicional

### Clasificación

| Elemento | Tipo | Justificación |
|---|---|---|
| El CSV de sensores | **Estructurado** | Tiene filas y columnas fijas, con un tipo de dato definido para cada columna (`temperatura_c` es numérica, `planta` es texto, etc.). |
| Un mensaje JSON enviado por un sensor | **Semiestructurado** | Tiene una organización por campos y valores (por ejemplo `"id_sensor": "S001"`), pero no está en una tabla rígida y los campos pueden variar entre mensajes. |
| Una fotografía de una máquina | **No estructurado** | Es una imagen sin campos ni columnas. Se necesitan técnicas de visión por computadora para extraer información de ella. |
| El texto libre de un reporte de mantenimiento | **No estructurado** | Es lenguaje natural escrito por una persona, sin formato fijo. Se necesitan técnicas de procesamiento de lenguaje para analizarlo. |

### ¿Por qué 100,000 registros no convierten al archivo en Big Data?

Big Data no depende solo de que haya muchos registros. Se habla de Big Data cuando el volumen, la velocidad y la variedad de los datos superan lo que se puede manejar con herramientas tradicionales en una sola computadora. Este archivo pesa unos pocos megabytes, `pandas` lo carga completo en la memoria y el programa lo analiza en un instante. Además, todos los datos son de un solo tipo (una tabla) y ya están guardados, no llegan en un flujo continuo. Por eso es un conjunto de datos pequeño, aunque 100,000 filas suene a mucho.

### Limitaciones al aumentar la escala

- **Memoria:** `pandas` carga todo el archivo en la RAM. Con cientos de millones de filas por día, el archivo ya no cabría en una sola computadora.
- **Tiempo de procesamiento:** el análisis tardaría cada vez más y el resultado llegaría tarde, por ejemplo al día siguiente.
- **Un solo equipo:** si esa computadora falla, se pierde el procesamiento. Haría falta repartir el trabajo entre varias máquinas.
- **Formato CSV:** no sirve bien para consultas rápidas ni para varios usuarios a la vez, y no guarda fotos ni textos de manera adecuada.
- **Datos que llegan sin parar:** un programa que lee un archivo cerrado no puede reaccionar a lecturas nuevas en el momento en que llegan.
- **Nuevos tipos de datos:** las fotografías y los reportes necesitan otras herramientas de almacenamiento y análisis, distintas a una tabla.

---

## 7. Batch y Streaming

### Tipo de procesamiento que realicé

Realicé **procesamiento por lotes (batch)**. El programa lee un archivo que ya está completo y guardado, procesa todos los registros juntos y entrega los resultados al final. No reacciona a lecturas nuevas, solo analiza un conjunto de datos cerrado, y no importa si el resultado tarda unos segundos o minutos en llegar.

### Alerta pocos segundos después de recibir una lectura mayor que 85 °C

Usaría **streaming** (procesamiento de flujos). Cada lectura se procesa en cuanto llega, y una regla sencilla (`temperatura > 85`) dispara la alerta de inmediato. Con herramientas como Apache Kafka para recibir los eventos y Spark Structured Streaming o Apache Flink para procesarlos, la alerta saldría en segundos. Si se espera al final del día, la alerta no serviría: la máquina ya habría pasado horas por encima del umbral.

### Resumen al terminar el día

Usaría **batch**. El resumen (promedios por planta, total de alertas, planta con más alertas, etc.) necesita todas las lecturas del día juntas y nadie lo necesita al instante. Un proceso programado que corra una vez al día, por ejemplo de madrugada, es más simple y barato que mantener un cálculo continuo.

### Relación con el tiempo en que se necesita cada resultado

| Necesidad | Tiempo en que se necesita el resultado | Enfoque |
|---|---|---|
| Alerta por temperatura alta | Segundos (una máquina puede dañarse) | Streaming |
| Resumen diario | Horas (basta con tenerlo al día siguiente) | Batch |

La regla que sigo es que mientras menos tiempo se pueda esperar por el resultado, más se justifica el streaming. Si se puede esperar, batch es más sencillo.

---

## 8. Lambda y Kappa

### Escenario A: ruta por lotes para el historial y ruta rápida para lo reciente

**Elijo la arquitectura Lambda.** Lambda tiene justo dos rutas: una **batch** que recalcula el historial completo con calma y otra **speed (rápida)** que procesa las lecturas recientes de inmediato. Una capa de servicio junta ambos resultados.

```
                    +--------------------------+
                 +->|  Capa batch              |--+
                 |  |  (recalcula el historial)|  |
+-----------+    |  +--------------------------+  |   +-------------+    +----------+
| Sensores  |----+                                +->| Capa de     |--->| Consultas|
| (lecturas)|    |  +--------------------------+  |   | servicio    |    | y alertas|
+-----------+    +->|  Capa rápida (speed)     |--+   +-------------+    +----------+
                    |  (procesa lo reciente)   |
                    +--------------------------+
```

Justificación: el historial recalculado por lotes es completo y exacto, y la ruta rápida da una respuesta inmediata sobre lo más reciente, aunque sea aproximada. El costo es mantener **dos** códigos de procesamiento distintos, lo que es más complejo.

### Escenario B: una sola lógica de eventos y conservar las mediciones para reprocesarlas

**Elijo la arquitectura Kappa.** Kappa usa una **sola** ruta de streaming para todo. Los eventos se conservan en un registro (log) durable, y cuando se necesita recalcular el historial se vuelven a reproducir desde ese registro con la misma lógica.

```
+-----------+    +-----------------------+    +------------------------+    +-------------+
| Sensores  |--->| Registro de eventos   |--->| Procesamiento de flujo |--->| Resultados  |
| (lecturas)|    | (se conservan todas)  |    | (una sola lógica)      |    | y alertas   |
+-----------+    +-----------------------+    +------------------------+    +-------------+
                           ^                              |
                           |   reprocesar cuando se       |
                           +------ necesite (replay) -----+
```

Justificación: hay una única lógica, así que no hay que mantener dos códigos. Si cambia una regla (por ejemplo el umbral), se reprocesan las mediciones guardadas con el código nuevo.

---

## 9. Analítica descriptiva, predictiva y prescriptiva

### Descriptiva (qué pasó)

1. **Hubo 6,954 lecturas con temperatura mayor que 85 °C**, el 6.95 % de las 100,000 mediciones.
2. **La Planta_3 es la que tiene más alertas, con 1,777**, seguida de Planta_1 (1,737), Planta_4 (1,732) y Planta_2 (1,708). La diferencia entre plantas es pequeña: la Planta_3 tuvo el 7.11 % de sus lecturas en alerta y las otras plantas entre 6.83 % y 6.95 %.

### Predictiva (qué podría pasar)

**Pregunta:** ¿Qué máquinas tienen más probabilidad de presentar una falla en los próximos 7 días?

Para investigarla necesitaría datos que el CSV no tiene:
- Historial de fallas y paros de cada máquina, que serviría para saber qué pasó después de cada alerta.
- Reportes y fechas de mantenimiento, para saber cuándo se revisó o reparó cada máquina.
- Datos de cada máquina: tipo, antigüedad, modelo, carga de trabajo.
- Lecturas durante un periodo mucho más largo (el CSV cubre solo unas 42 horas) para ver tendencias.
- Condiciones del entorno, como temperatura ambiente o turno de operación.

### Prescriptiva (qué hacer)

**Acción propuesta:** si el análisis predictivo indica que una máquina tiene riesgo alto de falla, programar una inspección de mantenimiento preventivo antes de que falle. Por ejemplo, revisar primero los sensores con más alertas, como el S027 (211 alertas), y las máquinas de la Planta_3.

Antes de decidir revisaría:
- Si el sensor funciona bien (calibración), porque una lectura alta puede ser un error del sensor y no un problema de la máquina.
- El historial de fallas y los reportes de mantenimiento de esa máquina.
- Si la vibración también está alta, aunque en los datos actuales la vibración promedio en las alertas (3.02 mm/s) es casi igual a la del resto (3.00 mm/s), así que no hay relación visible.
- El costo de detener la máquina frente al costo de una falla, y cuándo conviene programar la parada.

**Aclaración importante:** una lectura por encima de 85 °C es una alerta del ejercicio. Por sí sola no demuestra que la máquina vaya a fallar. Hay que combinarla con más información antes de tomar una decisión.
