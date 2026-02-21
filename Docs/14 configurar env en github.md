Perfecto. Estás viendo dos niveles distintos de **Variables en GitHub Actions**:

* **Environment variables**
* **Repository variables**

Te explico la diferencia técnica real.

---

# 🔹 1️⃣ Repository Variables

Ubicación:

```
Settings → Secrets and variables → Actions → Variables → Repository variables
```

## 📌 Qué son

Variables globales para TODO el repositorio.

## 📌 Alcance

* Disponibles para todos los workflows
* Disponibles para todos los jobs
* No requieren declarar `environment:` en el workflow

## 📌 Cómo se usan

```yaml
${{ vars.DB_HOST }}
```

## 📌 Cuándo usarlas

* Configuración general del repo
* URLs
* Flags
* Valores no sensibles compartidos

---

# 🔹 2️⃣ Environment Variables (Environment-level)

Ubicación:

```
Settings → Environments → (ej. staging / production)
```

Luego dentro de cada environment:

* Variables
* Secrets

## 📌 Qué son

Variables asociadas a un entorno específico (staging, prod, dev, etc.)

## 📌 Alcance

Solo se inyectan si tu workflow declara:

```yaml
environment: production
```

Ejemplo:

```yaml
jobs:
  deploy:
    environment: production
```

## 📌 Cómo se usan

```yaml
${{ vars.DB_HOST }}
```

Pero solo si el job usa ese `environment`.

## 📌 Cuándo usarlas

* Configuración distinta por entorno
* Staging ≠ Production
* Deploys controlados
* Cuando quieres approval manual antes de ejecutar

---

# 🎯 Diferencia clave

| Característica                  | Repository Variables  | Environment Variables     |
| ------------------------------- | --------------------- | ------------------------- |
| Alcance                         | Global repo           | Solo para ese environment |
| Requiere `environment:` en YAML | ❌ No                  | ✅ Sí                      |
| Ideal para                      | Configuración general | Configuración por entorno |
| Puede tener protection rules    | ❌ No                  | ✅ Sí                      |
| Puede requerir aprobación       | ❌ No                  | ✅ Sí                      |

---

# 🔥 Ejemplo real

## Repository variable

```
APP_NAME=FastAPIApp
```

Disponible siempre.

---

## Environment: production

Variables:

```
DB_HOST=prod-db.company.com
```

Workflow:

```yaml
jobs:
  deploy:
    environment: production
```

Solo ahí se inyecta.

---

# 🧠 Regla profesional

* 🔐 Secrets sensibles → `Secrets`
* 🌍 Configuración global → `Repository variables`
* 🚀 Configuración por entorno (staging/prod) → `Environment variables`

---

# ⚠️ Importante (seguridad)

En la parte superior de tu screenshot aparece:

> not passed to workflows that are triggered by a pull request from a fork.

Eso significa:

* **Secrets NO se exponen en PRs desde forks**
* Es una medida de seguridad
* Variables pueden comportarse distinto dependiendo del contexto

---

Si quieres, ahora te explico la diferencia entre:

* `vars`
* `env`
* `secrets`
* `environment`
* `repository_dispatch`
* `pull_request_target`

Porque ahí es donde muchos pipelines se rompen en producción.
