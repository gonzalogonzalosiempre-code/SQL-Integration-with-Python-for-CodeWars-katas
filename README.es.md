# Tracker de Katas de Codewars — Proyecto Final CS50P

[Read in English](README.md)

Herramienta de línea de comandos en Python que extrae tu historial real de katas resueltas en Codewars a través de su API pública, lo enriquece con el kyu de cada kata, guarda todo en una base de datos SQLite local, y genera estadísticas reales de progreso — por rango (kyu), por lenguaje, y por mes.

Construido como proyecto final para **CS50P de Harvard (Introducción a la Programación con Python)**.

---

## Video de demostración

- 🎥 **[https://youtu.be/tB8CSlqJB5U]()** — recorrido detallado del diseño y del código.
- 🎥 **[https://drive.google.com/file/d/1DyAaTQLEbotwMIqDyBtTHSrWmTArOkUA/view?usp=sharing]()** — la presentación obligatoria de 2-3 minutos.

---

## Qué hace

1. Trae tus challenges completados de Codewars desde la API pública (`/users/{usuario}/code-challenges/completed`)
2. Por cada kata, hace una segunda llamada al endpoint de detalle (`/code-challenges/{id}`) para obtener su kyu — un dato que el primer endpoint no incluye
3. Combina ambas fuentes en un solo registro por kata y lo guarda en `Datos.json`
4. Carga esos datos en una base de datos SQLite local (`katas.db`), creando la tabla si no existe
5. Ejecuta consultas SQL agregadas para mostrar el progreso por rango, por lenguaje, y por mes

---

## Por qué se construyó así

**Datos reales, no una demo genérica.** En vez de un CRUD inventado, el proyecto corre sobre el historial real de Codewars del autor — convirtiendo un ejercicio rutinario de "conectar una API con una base de datos" en algo con valor personal real.

**El rate limiting se respeta a propósito.** El endpoint de detalle se llama una vez por kata, con una pausa de `time.sleep(1)` entre peticiones. Disparar todas las llamadas de golpe (por ejemplo, con hilos) golpearía el límite de la API con más fuerza, no lo evitaría — y este es un script pensado para correr ocasionalmente, no un servicio de baja latencia, así que esperar no tiene ningún costo real.

**Se extrajeron funciones puras para poder testearlas.** Las funciones que tocan red o disco (`get_datos`, `sql_save`, `stats_request`) se mantienen separadas de funciones pequeñas y puras que solo transforman datos (`combined_datos`, `format_datos`, `extract_year_month`). Las funciones puras se pueden testear con simples `assert` y diccionarios simulados — sin necesitar red ni base de datos, que es exactamente lo que pide el requisito de `pytest` de CS50P.

**La lógica de agrupar por mes existe en dos lugares a propósito.** `extract_year_month()` es una función pura de Python (fácil de testear), y además se registra directamente dentro de SQLite mediante `conn.create_function()`, para poder usar exactamente la misma lógica en una consulta `GROUP BY`. Esto evita reimplementar la misma lógica de recorte de fechas dos veces en dos lenguajes distintos.

---

## Estructura del proyecto (según los requisitos de CS50P)

```
project.py          # main() + todas las funciones requeridas, al mismo nivel de indentación
test_project.py      # tests de 3 de las funciones puras, con prefijo test_
requirements.txt      # requests, pytest
README.md / README.es.md
```

### Funciones en `project.py`

| Función | Propósito | ¿Toca red/disco? |
|---|---|---|
| `main()` | Orquesta el flujo completo | — |
| `get_datos()` | Trae la lista de challenges completados y, por cada uno, su detalle de rango | Sí (red + archivo) |
| `combined_datos(kata, detalle)` | Combina el registro de una kata con su detalle en un solo diccionario | No — pura |
| `format_datos(lista)` | Convierte una lista de lenguajes en un solo string separado por espacios | No — pura |
| `sql_save(datos)` | Crea la tabla e inserta los registros combinados | Sí (archivo + base de datos) |
| `stats_request(database)` | Ejecuta las consultas `GROUP BY` e imprime los resultados | Sí (base de datos) |
| `extract_year_month(fecha)` | Recorta un string de fecha ISO hasta `YYYY-MM` | No — pura |

---

## Cómo correrlo

```bash
pip install -r requirements.txt
python project.py
```

Edita el nombre de usuario en la URL de la API dentro de `get_datos()` antes de correrlo con tu propia cuenta.

## Cómo correr los tests

```bash
pytest test_project.py -v
```

Tres tests cubren las tres funciones puras (`combined_datos`, `format_datos`, `extract_year_month`) usando datos simulados — no se necesita conexión a la API real ni acceso a la base de datos para correrlos.

---

## Ejemplo de salida

```
('2 kyu', 1)
('3 kyu', 1)
('4 kyu', 8)
('5 kyu', 5)
('6 kyu', 15)
('7 kyu', 4)
('8 kyu', 4)

('cpp', 34)
('python', 1)
('sql', 3)

('2026-05', 2)
('2026-06', 8)
('2026-08', 17)
('2026-09', 11)
```

---

## Una historia real de depuración que vale la pena mencionar

Durante el desarrollo, el proyecto se topó con una cadena de bugs sutil pero instructiva: una confusión de entornos de Python (el comando `python` resolvía silenciosamente a otra instalación distinta e incompleta, agregada al PATH por otra herramienta), combinada con un problema de archivo sin guardar, donde la terminal seguía ejecutando una versión vieja de `project.py` (previa a la refactorización) sin ningún error visible. Ambos solo se encontraron agregando puntos de verificación explícitos con `print` y confirmando directamente `sys.executable` y `dir(modulo)` — un recordatorio de que "no mostrar ningún error" no significa "el código que corrió es el que crees que corrió".

---

## Posibles extensiones

- Guardar las estadísticas por lenguaje en una tabla relacional propia (técnicamente una kata puede resolverse en más de un lenguaje)
- Cachear las respuestas de la API para no volver a pedir detalles de katas ya conocidas
- Un pequeño menú de CLI en vez de una ejecución lineal única de `main()`
