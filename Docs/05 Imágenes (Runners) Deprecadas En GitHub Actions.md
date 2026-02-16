<!-- Autor: Daniel Benjamin Perez Morales -->
<!-- GitHub: https://github.com/D4nitrix13 -->
<!-- GitLab: https://gitlab.com/D4nitrix13 -->
<!-- Correo electrónico: danielperezdev@proton.me -->

# Imágenes (Runners) Deprecadas en GitHub Actions

## ¿Qué es una imagen en `runs-on`?

Cuando defines:

```yaml
runs-on: ubuntu-latest
```

Estás indicando qué **imagen de máquina virtual (runner)** debe usar GitHub para ejecutar tu job.

Esa imagen contiene:

* Sistema operativo
* Versión del kernel
* Herramientas preinstaladas (git, node, python, docker, etc.)
* Librerías base

GitHub mantiene estas imágenes actualizadas periódicamente.

---

## 🔴 ¿Qué significa que una imagen esté "deprecated"?

Una imagen deprecada significa que:

* Ya no recibe actualizaciones de seguridad
* Puede dejar de estar disponible en cualquier momento
* Puede causar jobs en estado `Queued` indefinidamente
* Puede generar fallos inesperados

Ejemplo típico:

```yaml
runs-on: ubuntu-latest
```

Ubuntu latest ya está fuera de soporte (EOL), por lo tanto GitHub dejó de recomendar su uso.

---

## 🟡 Síntomas comunes de una imagen deprecada

* El job se queda en estado:

  * `Queued`
  * `Waiting for a runner`
* El workflow tarda demasiado en iniciar
* Mensajes en logs indicando que la imagen está obsoleta

---

## ✅ Solución recomendada

Usar imágenes activas y soportadas:

```yaml
runs-on: ubuntu-latest
```

O especificar una versión LTS actual:

```yaml
runs-on: ubuntu-22.04
```

---

## 🧠 Diferencia entre `ubuntu-latest` y versión fija

### `ubuntu-latest`

✔ Siempre apunta a la versión estable más reciente
✔ Recibe mejoras automáticas
⚠ Puede cambiar de versión en el futuro

### `ubuntu-22.04`

✔ Versión fija y predecible
✔ Ideal para entornos productivos
✔ Mayor estabilidad a largo plazo

---

## 🎯 Buenas prácticas profesionales

1. Para proyectos personales o CI general:

   ```yaml
   runs-on: ubuntu-latest
   ```

2. Para pipelines críticos o producción:

   ```yaml
   runs-on: ubuntu-22.04
   ```

3. Evitar versiones EOL como:

   * ubuntu-latest
   * ubuntu-16.04

---

## 🔎 Cómo saber si una imagen está deprecada

GitHub publica el estado oficial de runners en:

[https://github.com/actions/runner-images](https://github.com/actions/runner-images)

Ahí puedes ver:

* Versiones activas
* Fechas de deprecación
* Cambios de versión

---

## 📌 Conclusión técnica

El campo `runs-on` no es solo una preferencia de sistema operativo;
define la base de ejecución del pipeline.

Usar imágenes deprecadas puede causar:

* Fallos intermitentes
* Bloqueo de jobs
* Problemas de seguridad
* Inconsistencias en builds

Por eso es fundamental mantener actualizada la versión del runner.
