# Codewars Kata Tracker — CS50P Final Project

[Leer en español](README.es.md)

A Python command-line tool that pulls your real Codewars solving history through the public API, enriches it with per-kata rank data, stores everything in a local SQLite database, and generates real progress statistics — by rank (kyu), by language, and by month.

Built as the final project for **Harvard's CS50P (Introduction to Programming with Python)**.

---

## Video Demo

- 🎥 **[https://youtu.be/HfKBim6dx5o]()** — detailed explanation of the design and code.
- 🎥 **[https://youtu.be/tB8CSlqJB5U]()** — the required 2–3 minute presentation.

---

## What It Does

1. Fetches your completed Codewars challenges from the public API (`/users/{username}/code-challenges/completed`)
2. For each kata, makes a second call to the kata detail endpoint (`/code-challenges/{id}`) to retrieve its rank (kyu) — a field the first endpoint doesn't include
3. Combines both sources into a single record per kata and saves it to `Datos.json`
4. Loads that data into a local SQLite database (`katas.db`), creating the table if it doesn't exist
5. Runs aggregate SQL queries to show progress by rank, by language, and by month

---

## Why It Was Built This Way

**Real data, not a generic demo.** Instead of a made-up CRUD app, the project runs on the author's actual Codewars history — turning a routine "connect to an API and a database" exercise into something with real personal value.

**Rate limiting is respected on purpose.** The kata detail endpoint is called once per kata, with a `time.sleep(1)` between requests. Firing all requests at once (e.g., with threads) would hit the API's rate limit harder, not avoid it — and this is a script meant to run occasionally, not a low-latency service, so there's no real cost to waiting.

**Pure functions were pulled out for testability.** Functions that touch the network or the filesystem (`get_datos`, `sql_save`, `stats_request`) are kept separate from small, pure functions that only transform data (`combined_datos`, `format_datos`, `extract_year_month`). The pure functions can be tested with plain `assert` statements and mock dictionaries — no network or database required, which is exactly what CS50P's `pytest` requirement calls for.

**The month-grouping logic exists in two places on purpose.** `extract_year_month()` is a pure Python function (easy to unit test), and it's also registered directly inside SQLite via `conn.create_function()` so the exact same logic can be used in a `GROUP BY` query. This avoids reimplementing the same date-slicing logic twice in two different languages.

---

## Project Structure (per CS50P requirements)

```
project.py          # main() + all required functions, same indentation level
test_project.py      # tests for 3 of the pure functions, prefixed with test_
requirements.txt      # requests, pytest
README.md / README.es.md
```

### Functions in `project.py`

| Function | Purpose | Touches network/disk? |
|---|---|---|
| `main()` | Orchestrates the full flow | — |
| `get_datos()` | Fetches the completed-challenges list and, per kata, its rank detail | Yes (network + file) |
| `combined_datos(kata, detalle)` | Merges a kata record with its detail into one dict | No — pure |
| `format_datos(lista)` | Turns a list of languages into a single space-joined string | No — pure |
| `sql_save(datos)` | Creates the table and inserts the combined records | Yes (file + database) |
| `stats_request(database)` | Runs the `GROUP BY` queries and prints the results | Yes (database) |
| `extract_year_month(fecha)` | Slices an ISO date string down to `YYYY-MM` | No — pure |

---

## Running It

```bash
pip install -r requirements.txt
python project.py
```

Edit the username in the API URL inside `get_datos()` before running it with your own account.

## Running the Tests

```bash
pytest test_project.py -v
```

Three tests cover the three pure functions (`combined_datos`, `format_datos`, `extract_year_month`) using mock data — no live API calls or database access needed to run them.

---

## Example Output

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

## A Real Debugging Story Worth Mentioning

During development, the project ran into a subtle but instructive bug chain: a Python environment mix-up (the `python` command was silently resolving to a different, incomplete Python installation added to PATH by another toolchain), combined with an unsaved-file issue where the terminal kept executing a stale, pre-refactor version of `project.py` without any visible error. Both were only found by adding explicit print-based checkpoints and verifying `sys.executable` and `dir(module)` directly — a reminder that "no error shown" doesn't mean "the code that ran is the code you think ran."

---

## Possible Extensions

- Store per-language stats as a proper relational table (a kata can technically be solved in more than one language)
- Cache the API responses to avoid re-fetching kata details already known
- A small CLI menu instead of a single linear `main()` run
