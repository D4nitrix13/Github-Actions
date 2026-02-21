Perfecto. Vamos a construir un **workflow profesional** que:

1. 🔹 Levante un servicio PostgreSQL en GitHub Actions
2. 🔹 Se conecte usando:

   * Variables explícitas
   * Variables de entorno definidas en el workflow
   * Secrets de GitHub
3. 🔹 Ejecute un test de conexión real

Te daré **3 variantes claras y separadas**.

---

# 🧩 1️⃣ Workflow con variables explícitas (hardcoded)

Archivo:

```
.github/workflows/postgres-explicit-env.yml
```

```yaml
name: PostgreSQL Integration Test (Explicit Environment Variables)

on:
  workflow_dispatch:

jobs:
  postgres-explicit-connection:
    name: Connect to PostgreSQL Using Explicit Variables
    runs-on: ubuntu-latest
    timeout-minutes: 10

    services:
      postgres:
        image: postgres:latest
        env:
          POSTGRES_USER: explicit_user
          POSTGRES_PASSWORD: explicit_password
          POSTGRES_DB: explicit_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd="pg_isready -U explicit_user"
          --health-interval=10s
          --health-timeout=5s
          --health-retries=5

    steps:
      - name: Install PostgreSQL Client
        run: sudo apt-get update && sudo apt-get install -y postgresql-client

      - name: Test Connection with Explicit Variables
        run: |
          PGPASSWORD=explicit_password psql \
          -h localhost \
          -U explicit_user \
          -d explicit_db \
          -c "SELECT version();"
```

---

# 🧩 2️⃣ Workflow usando variables de entorno del workflow (`env:`)

```
.github/workflows/postgres-workflow-env.yml
```

```yaml
name: PostgreSQL Integration Test (Workflow Environment Variables)

on:
  workflow_dispatch:

env:
  DB_USER: workflow_user
  DB_PASSWORD: workflow_password
  DB_NAME: workflow_db
  DB_HOST: localhost
  DB_PORT: 5432

jobs:
  postgres-env-connection:
    name: Connect to PostgreSQL Using Workflow Env
    runs-on: ubuntu-latest
    timeout-minutes: 10

    services:
      postgres:
        image: postgres:latest
        env:
          POSTGRES_USER: ${{ env.DB_USER }}
          POSTGRES_PASSWORD: ${{ env.DB_PASSWORD }}
          POSTGRES_DB: ${{ env.DB_NAME }}
        ports:
          - 5432:5432
        options: >-
          --health-cmd="pg_isready -U ${{ env.DB_USER }}"
          --health-interval=10s
          --health-timeout=5s
          --health-retries=5

    steps:
      - name: Install PostgreSQL Client
        run: sudo apt-get update && sudo apt-get install -y postgresql-client

      - name: Test Connection with Workflow Env
        run: |
          PGPASSWORD=${{ env.DB_PASSWORD }} psql \
          -h ${{ env.DB_HOST }} \
          -U ${{ env.DB_USER }} \
          -d ${{ env.DB_NAME }} \
          -c "SELECT current_database();"
```

---

# 🧩 3️⃣ Workflow usando GitHub Secrets (recomendado producción)

Primero crea secrets en tu repo:

Settings → Secrets and variables → Actions → New repository secret

Ejemplo:

* `POSTGRES_USER`
* `POSTGRES_PASSWORD`
* `POSTGRES_DB`

---

```
.github/workflows/postgres-secrets.yml
```

```yaml
name: PostgreSQL Integration Test (Using GitHub Secrets)

on:
  workflow_dispatch:

jobs:
  postgres-secrets-connection:
    name: Connect to PostgreSQL Using Secrets
    runs-on: ubuntu-latest
    timeout-minutes: 10

    services:
      postgres:
        image: postgres:latest
        env:
          POSTGRES_USER: ${{ secrets.POSTGRES_USER }}
          POSTGRES_PASSWORD: ${{ secrets.POSTGRES_PASSWORD }}
          POSTGRES_DB: ${{ secrets.POSTGRES_DB }}
        ports:
          - 5432:5432
        options: >-
          --health-cmd="pg_isready -U ${{ secrets.POSTGRES_USER }}"
          --health-interval=10s
          --health-timeout=5s
          --health-retries=5

    steps:
      - name: Install PostgreSQL Client
        run: sudo apt-get update && sudo apt-get install -y postgresql-client

      - name: Test Connection Using Secrets
        env:
          PGPASSWORD: ${{ secrets.POSTGRES_PASSWORD }}
        run: |
          psql \
          -h localhost \
          -U ${{ secrets.POSTGRES_USER }} \
          -d ${{ secrets.POSTGRES_DB }} \
          -c "SELECT now();"
```

---

# 🧠 Diferencia entre los 3 enfoques

| Método               | Seguridad | Uso            |
| -------------------- | --------- | -------------- |
| Variables explícitas | ❌ Baja    | Testing rápido |
| `env:` en workflow   | ⚠️ Media   | Entornos CI    |
| GitHub Secrets       | ✅ Alta    | Producción     |

---

# 🎯 Profesionalmente correcto

En CI real se usa:

* Secrets para credenciales
* `env:` para configuración no sensible
* Services para levantar contenedores
* Healthcheck obligatorio

---

Si quieres, ahora podemos:

* Integrarlo con tu FastAPI + pytest
* Hacer que corra migraciones
* Levantar Postgres + Redis simultáneamente
* O simular entorno docker-compose dentro de Actions

¿Quieres integración real con tu app FastAPI ahora?

---

Excelente pregunta.

`workflow_dispatch` es un **evento manual** en GitHub Actions.

---

# 📌 ¿Cuándo se ejecuta?

Un workflow con:

```yaml
on:
  workflow_dispatch:
```

👉 **NO se ejecuta automáticamente.**

Solo se ejecuta cuando tú lo disparas manualmente.

---

# 🖱 Cómo se ejecuta

1. Ve a tu repositorio en GitHub
2. Click en **Actions**
3. Selecciona el workflow
4. Click en **“Run workflow”**
5. Elegir branch
6. Confirmar

---

# 🧠 ¿Para qué sirve?

Se usa cuando:

* 🔹 Quieres ejecutar pruebas bajo demanda
* 🔹 Ejecutar scripts de mantenimiento
* 🔹 Desplegar manualmente
* 🔹 Probar conexión a base de datos
* 🔹 Ejecutar migraciones controladas

No es para CI automático típico.

---

# 📌 Comparación con otros triggers

| Trigger             | Cuándo se ejecuta          |
| ------------------- | -------------------------- |
| `push`              | Cada vez que haces push    |
| `pull_request`      | Cuando abres/actualizas PR |
| `workflow_dispatch` | Manual                     |
| `schedule`          | Por cron                   |
| `release`           | Cuando se crea un release  |

---

# 🎯 Ejemplo híbrido (muy común)

```yaml
on:
  push:
    branches: [master]
  workflow_dispatch:
```

Eso significa:

* Se ejecuta automáticamente en push
* También puedes ejecutarlo manualmente cuando quieras

---

# 🔥 Bonus avanzado

Puedes agregar inputs al `workflow_dispatch`:

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: "Environment to deploy"
        required: true
        default: "staging"
```

Y luego usarlo:

```yaml
${{ github.event.inputs.environment }}
```

Eso permite parametrizar ejecuciones manuales.

---

Si quieres, te explico también:

* Diferencia entre `repository_dispatch` y `workflow_dispatch`
* Cómo disparar workflows desde otro workflow
* Cómo crear pipelines multi-stage manuales

¿Seguimos?
