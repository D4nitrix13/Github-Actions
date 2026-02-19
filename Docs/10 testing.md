Para hacer **testing en GitHub Actions** (Python/FastAPI), lo normal es correr **pytest** en cada `push` y `pull_request`, y hacer que el workflow **falle** si algún test falla.

Aquí tienes una configuración **bien nombrada y compatible con `uv` + `pyproject.toml`**.

---

## 1) Instala pytest como dev dependency (uv)

En tu `pyproject.toml` (ejemplo con uv):

```toml
[tool.uv]
dev-dependencies = [
  "pytest",
  "pytest-cov",
]
```

Luego (local):

```bash
uv sync
```

---

## 2) Crea tests básicos

Estructura recomendada:

```
tests/
  test_health.py
```

`tests/test_health.py`:

```python
def test_sanity_check() -> None:
    assert 1 + 1 == 2
```

---

## 3) Workflow de GitHub Actions para correr tests

Crea:

```
.github/workflows/python-tests.yml
```

```yaml
name: Python Test Suite Execution

on:
  push:
    branches: [master]
  pull_request:

jobs:
  unit-and-integration-tests:
    name: Run Pytest Unit Tests with Coverage
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout Repository Source Code
        uses: actions/checkout@v4

      - name: Install uv Dependency Manager
        uses: astral-sh/setup-uv@v7

      - name: Synchronize Project Dependencies (Locked)
        run: uv sync --frozen

      - name: Execute Pytest Test Suite
        run: uv run pytest -q

      - name: Generate Coverage Report
        run: uv run pytest --cov=. --cov-report=term-missing -q
```

> Si no quieres correr pytest dos veces, deja solo el de coverage.

---

## 4) (Opcional) Integrarlo con tu workflow de Ruff + MyPy

Puedes tener **un solo workflow** con 2 jobs:

* `static-analysis` (ruff + mypy)
* `test-suite` (pytest)

Así se ejecutan en paralelo y es más limpio.

---

## Tips rápidos (para que no se “cuelgue”)

* **No apuntes a `.` si tu repo incluye `.venv/`**; exclúyelo o apunta a `src/` / tu carpeta real.
* Pon `timeout-minutes` (ya lo puse).
* Si usas base de datos después, puedes levantar Postgres como service en Actions.

---

Si me dices cómo se llama tu archivo principal (¿`main.py`?) y tu estructura (¿`src/` o raíz?), te dejo un ejemplo de **test real** para FastAPI usando `TestClient` (GET `/` y POST `/users`).

---

Entendido: **ya existe `src/__init__.py`**, así que el fallo no era “no es paquete”. Entonces el motivo real es este:

✅ **Tu `src/` no está en el `PYTHONPATH` durante `uv run pytest`**, por eso Python no encuentra el paquete `src` aunque exista.

En otras palabras: tener `src/__init__.py` no basta si **la raíz del repo** no está en el path de imports (o si pytest está ejecutando con un cwd/paths distintos).

Aquí tienes 3 soluciones correctas (de más “limpia” a más “rápida”). Elige una.

---

## Solución 1 (recomendada): `tests/conftest.py` agrega la raíz al `sys.path`

Crea `tests/conftest.py`:

```python
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT: str = str(Path(__file__).resolve().parents[1])
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
```

Y deja tu import como lo tenías:

```py
from src.main import app, fake_users_db
```

👉 Esto hace que `src` sea importable siempre en tests, local y en GitHub Actions.

---

## Solución 2 (más pro): declarar `PYTHONPATH` en el workflow / ejecución

Local:

```bash
PYTHONPATH=. uv run pytest -q
```

En GitHub Actions:

```yaml
- name: Execute Pytest Test Suite
  run: PYTHONPATH=. uv run pytest -q
```

---

## Solución 3 (la más “correcta” a largo plazo): instalar el proyecto como paquete

Esto evita hacks de path, pero requiere que tu `pyproject.toml` esté configurado como paquete instalable (setuptools/hatch/poetry, etc.).
Si me pegas tu `pyproject.toml`, te lo dejo perfecto en 2 minutos.

---

# Por qué te pasa aunque exista `src/__init__.py`

Porque Python solo puede importar `src` si puede ver el **directorio padre** de `src` (la raíz del repo).
Si ese directorio no está en `sys.path`, `import src.main` falla.

---

## Qué haría yo en tu caso (rápido y estable)

✅ `tests/conftest.py` (Solución 1) + mantener imports limpios.

Si quieres, pégame tu `tests/test_users_api.py` actual y te lo ajusto exacto (incluyendo el fixture que limpia `fake_users_db`).

---
Buena pregunta — y aquí está la clave técnica:

👉 **`conftest.py` no se importa manualmente.**
Pytest lo **descubre automáticamente**.

---

## 🔎 Cómo funciona realmente

Cuando ejecutas:

```bash
uv run pytest
```

Pytest:

1. Recorre el árbol de directorios buscando:

   * `test_*.py`
   * `*_test.py`
   * `conftest.py`

2. Cuando encuentra un `conftest.py`:

   * Lo carga automáticamente
   * Ejecuta su código
   * Registra fixtures
   * Modifica `sys.path` si tú lo haces ahí

No necesitas hacer:

```python
import conftest
```

Eso sería incorrecto.

---

## 🎯 Entonces, ¿por qué se solucionó?

Porque dentro de `conftest.py` agregaste esto:

```python
PROJECT_ROOT: str = str(Path(__file__).resolve().parents[1])
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
```

Eso ejecuta en el momento en que pytest carga `conftest.py`, antes de importar tus tests.

Entonces cuando el test hace:

```python
from src.main import app
```

Ya existe el path correcto en `sys.path`.

---

## 🧠 Orden real de ejecución

1. pytest inicia
2. encuentra `conftest.py`
3. ejecuta `conftest.py`
4. modifica `sys.path`
5. recién ahí importa `tests/test_users_api.py`
6. ahora `src.main` sí es importable

---

## 📌 Por eso nunca se importa manualmente

`conftest.py` es un **hook file especial de pytest**, no un módulo tradicional.

---

Si quieres, te explico ahora:

* Cómo funciona el discovery system interno de pytest
* Cómo funcionan los fixtures autouse
* Cómo convertir tu proyecto en instalable y eliminar `sys.path` hacks

Tú decides el siguiente nivel.

---

`.coverage` es el **archivo binario que genera `coverage.py` (o `pytest-cov`)** cuando ejecutas tests con medición de cobertura.

No es código fuente.
No es texto plano.
Es una **base de datos SQLite interna** donde se guarda qué líneas fueron ejecutadas.

---

# 📌 ¿Cuándo se crea?

Cuando ejecutas algo como:

```bash
uv run pytest --cov=.
```

o

```bash
coverage run -m pytest
```

Entonces se genera en la raíz del proyecto:

```
.coverage
```

---

# 📦 ¿Qué contiene?

Guarda:

* Archivos analizados
* Líneas ejecutadas
* Líneas no ejecutadas
* Metadata de ejecución

Internamente usa SQLite.

---

# 📊 ¿Cómo se usa?

Después puedes generar reportes:

### Reporte en consola

```bash
uv run coverage report
```

### Reporte HTML

```bash
uv run coverage html
```

Eso crea:

```
htmlcov/
```

Y puedes abrir:

```
htmlcov/index.html
```

---

# 🧠 Flujo típico profesional

```bash
uv run pytest --cov=src --cov-report=term-missing
```

Luego:

```bash
uv run coverage html
```

---

# 🚫 ¿Debe subirse al repo?

No.

Agrega esto a `.gitignore`:

```
.coverage
htmlcov/
```

Porque:

* Es artefacto temporal
* Cambia en cada ejecución
* No es código fuente

---

# 🎯 Diferencia entre cosas relacionadas

| Archivo        | Qué es                            |
| -------------- | --------------------------------- |
| `.coverage`    | Base de datos interna de coverage |
| `htmlcov/`     | Reporte visual HTML               |
| `.mypy_cache/` | Cache de mypy                     |
| `.ruff_cache/` | Cache de ruff                     |

Todos son artefactos generados.

---

Si quieres, ahora te explico cómo:

* Hacer que GitHub Actions falle si cobertura < 80%
* Subir cobertura a Codecov
* Generar badge dinámico en README
* O hacer quality gate completo estilo enterprise

¿Seguimos con coverage enforcement?
