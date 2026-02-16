<!-- Autor: Daniel Benjamin Perez Morales -->
<!-- GitHub: https://github.com/D4nitrix13 -->
<!-- GitLab: https://gitlab.com/D4nitrix13 -->
<!-- Correo electrónico: danielperezdev@proton.me -->

# 🧩 Explicación detallada de los comandos utilizados

## 1️⃣ `mkdir my-api`

```bash
mkdir my-api
```

- **¿Qué hace?**

Crea un nuevo directorio llamado `my-api`.

- ¿Por qué es necesario?

Porque es buena práctica que cada proyecto Python:

- Tenga su propia carpeta
- Mantenga dependencias aisladas
- Tenga su propio `pyproject.toml`

Evita mezclar múltiples proyectos en el mismo directorio.

---

## 2️⃣ `cd my-api`

```bash
cd my-api
```

- **¿Qué hace?**

Cambia el directorio actual al proyecto recién creado.

### ¿Por qué es importante?

`uv` busca un archivo `pyproject.toml` en el directorio actual o en sus padres.

Si no estás dentro del proyecto, `uv` no sabrá dónde registrar dependencias.

---

## 3️⃣ `uv init`

```bash
uv init
```

- **¿Qué hace?**

Inicializa un proyecto Python moderno creando:

```bash
pyproject.toml
```

### ¿Qué es `pyproject.toml`?

Es el archivo estándar de configuración del proyecto Python moderno (PEP 621).

Contiene:

- Nombre del proyecto
- Versión
- Dependencias
- Metadatos

- ¿Qué ocurre internamente?

- Crea la estructura base del proyecto
- Define un entorno gestionado por `uv`
- Permite agregar dependencias declarativas

Sin este archivo, `uv add` no puede funcionar.

---

## 4️⃣ `uv add "fastapi[standard]"`

```bash
uv add "fastapi[standard]"
```

- **¿Qué hace?**

Agrega FastAPI como dependencia del proyecto.

### ¿Qué significa `[standard]`?

Es un *extra*. Instala dependencias adicionales recomendadas como:

- `uvicorn`
- `pydantic`
- herramientas de producción

- ¿Qué ocurre internamente?

1. Modifica `pyproject.toml`
2. Resuelve el árbol de dependencias
3. Crea/actualiza el archivo `uv.lock`
4. Crea automáticamente un entorno virtual
5. Instala los paquetes en ese entorno

---

## 5️⃣ `uv add uvicorn`

```bash
uv add uvicorn
```

- **¿Qué hace?**

Instala el servidor ASGI que ejecuta la aplicación FastAPI.

- ¿Por qué es necesario?

FastAPI define la aplicación, pero no ejecuta el servidor HTTP.

`uvicorn` es quien:

- Escucha en un puerto
- Recibe requests HTTP
- Ejecuta la aplicación ASGI

---

## 6️⃣ Crear `main.py`

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}
```

### ¿Qué hace este código?

1. Importa FastAPI
2. Crea una instancia de aplicación ASGI
3. Define una ruta GET `/`

Cuando el servidor recibe una petición a `/`, devuelve JSON.

---

## 7️⃣ `uv run uvicorn main:app --reload`

```bash
uv run uvicorn main:app --reload
```

### ¿Qué hace `uv run`?

Ejecuta un comando dentro del entorno virtual gestionado por `uv`.

Equivalente conceptual a:

```bash
source .venv/bin/activate
uvicorn main:app --reload
```

Pero sin activar manualmente.

---

### ¿Qué significa `main:app`?

- `main` → archivo `main.py`
- `app` → variable dentro de ese archivo

Es el import string:

```python
from main import app
```

---

### ¿Qué hace `--reload`?

Activa modo desarrollo:

- Detecta cambios en archivos
- Reinicia automáticamente el servidor

Ideal para desarrollo, no para producción.

---

## Comparación conceptual

| Comando | Qué hace realmente                 |
| ------- | ---------------------------------- |
| mkdir   | Crea espacio aislado del proyecto  |
| cd      | Posiciona el contexto de ejecución |
| uv init | Inicializa proyecto moderno        |
| uv add  | Gestiona dependencias declarativas |
| uv run  | Ejecuta dentro del entorno virtual |
| uvicorn | Ejecuta servidor ASGI              |

---

## 🏗 Flujo completo explicado

```bash
mkdir my-api        # Crear proyecto
cd my-api           # Entrar al proyecto
uv init             # Crear pyproject.toml
uv add fastapi      # Declarar dependencia
uv add uvicorn      # Instalar servidor
uv run uvicorn main:app --reload  # Ejecutar app
```

---

## 🎯 ¿Por qué usar `uv` y no `pip`?

`uv`:

✔ Gestiona dependencias declarativamente
✔ Genera lockfile reproducible
✔ Crea entorno virtual automáticamente
✔ Es más rápido que pip
✔ Está alineado con el estándar moderno de Python

`pip` tradicional:

- No crea proyecto
- No genera lockfile reproducible por defecto
- No maneja entorno automáticamente

---

## 🔐 Importante en CI/CD

En un pipeline GitHub Actions usarías algo como:

```yaml
- name: Install dependencies
  run: uv sync
```

En lugar de:

```yaml
pip install -r requirements.txt
```

Porque `uv sync` instala exactamente lo definido en `uv.lock`.

---

Si quieres, ahora podemos:

- Agregar cómo integrar esto en GitHub Actions
- Crear workflow completo para FastAPI
- Agregar Dockerfile optimizado
- Hacer versión production-ready con Gunicorn

¿Seguimos a integración CI/CD real?
