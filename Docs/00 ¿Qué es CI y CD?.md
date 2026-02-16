<!-- Autor: Daniel Benjamin Perez Morales -->
<!-- GitHub: https://github.com/D4nitrix13 -->
<!-- GitLab: https://gitlab.com/D4nitrix13 -->
<!-- Correo electrónico: danielperezdev@proton.me -->

# ¿Qué es CI y CD?

**CI/CD** es un conjunto de prácticas de **DevOps** orientadas a automatizar la integración, validación y despliegue del software.

* **CI (Continuous Integration – Integración Continua)**
* **CD (Continuous Delivery o Continuous Deployment – Entrega/Despliegue Continuo)**

---

## 1️⃣ CI – Continuous Integration

**Definición técnica:**
Proceso mediante el cual los desarrolladores integran cambios de código frecuentemente (varias veces al día) en una rama principal (ej. `main`), activando pipelines automáticos que ejecutan:

* Build
* Tests (unitarios, integración)
* Linting / análisis estático
* Validaciones de seguridad

### 🎯 Objetivo

Detectar errores lo antes posible y evitar “integration hell”.

### 🔄 Flujo típico de CI

1. Developer hace `git push`
2. Se dispara un pipeline (GitHub Actions, GitLab CI, etc.)
3. Se ejecutan:

   * `composer install`
   * `php artisan test`
   * `npm run build`
4. Si todo pasa → el código es aceptado
5. Si falla → se bloquea el merge

---

## 2️⃣ CD – Continuous Delivery vs Continuous Deployment

Aquí hay una distinción importante:

### 📦 Continuous Delivery

El sistema:

* Compila
* Testea
* Genera artefactos (Docker image, build)
* Los deja listos para producción

Pero **el deploy es manual** (ej. presionar botón).

---

### 🚀 Continuous Deployment

Después de pasar todos los tests:

➡️ Se despliega automáticamente a producción
Sin intervención humana.

---

## 🧠 ¿Para qué sirve CI/CD?

| Beneficio                 | Explicación                             |
| ------------------------- | --------------------------------------- |
| Detectar errores temprano | Los tests corren en cada commit         |
| Integraciones frecuentes  | Se evita acumulación de cambios grandes |
| Deploy más rápido         | Automatización reduce errores humanos   |
| Más seguridad             | Se pueden integrar escáneres SAST/DAST  |
| Artefactos reproducibles  | Builds consistentes vía Docker          |

---

## 🔧 Herramientas comunes

* **GitHub Actions**
* **GitLab CI/CD**
* **Jenkins**
* **CircleCI**
* **Azure DevOps**
* **Bitbucket Pipelines**

---

## 📌 Resumen conceptual

CI = Automatizar validación del código
CD = Automatizar entrega/despliegue
