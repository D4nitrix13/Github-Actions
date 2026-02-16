<!-- Autor: Daniel Benjamin Perez Morales -->
<!-- GitHub: https://github.com/D4nitrix13 -->
<!-- GitLab: https://gitlab.com/D4nitrix13 -->
<!-- Correo electrónico: danielperezdev@proton.me -->

# Indicadores de estado en GitHub Actions

Cuando un workflow se ejecuta, vas a ver un **icono** que refleja el estado del run:

* 🟡 **Amarillo** = *En progreso* (running) o *en cola* (queued)
* ✅ **Verde** = *Éxito* (passed / success)
* ❌ **Rojo** = *Falló* (failed)
* ⚪/🚫 (a veces) = *Cancelado* o *saltado* (cancelled / skipped)

Dónde se ve:

1. **En la pestaña Actions** del repo (lista de ejecuciones).
2. En algunos casos, también **junto al commit** y en los **Pull Requests** como “checks”.

## Ver detalles (logs)

Al dar click al run (o al icono/estado), podés ver:

* El workflow que corrió (por ejemplo: `Server`)
* El job (por ejemplo: `hello_world`)
* Los steps y sus logs (por ejemplo: “Echo the message”)

Ruta típica:
**Repo → Actions → Server → run → hello_world → logs**

## Nota importante (por qué a veces no lo ves donde esperás)

* Si tu repo **no tiene PR**, lo verás sobre todo en **Actions**.
* En el listado de commits, los checks pueden tardar un poco en aparecer o depender de cómo estés viendo GitHub (y de si el workflow aplica a ese commit).

Si querés, te lo redacto como un párrafo “listo para README” con tu estilo de documentación (y con el enlace tipo `https://github.com/<user>/<repo>/actions`).
