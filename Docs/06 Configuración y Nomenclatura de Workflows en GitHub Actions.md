<!-- Autor: Daniel Benjamin Perez Morales -->
<!-- GitHub: https://github.com/D4nitrix13 -->
<!-- GitLab: https://gitlab.com/D4nitrix13 -->
<!-- Correo electrónico: danielperezdev@proton.me -->

# 📁 Ubicación obligatoria

Deben estar dentro de:

```bash
.github/workflows/
```

Ejemplos válidos:

```bash
.github/workflows/ci.yml
.github/workflows/deploy.yaml
```

---

## ⚙️ ¿Hay diferencia técnica?

No.

`.yml` y `.yaml` son exactamente el mismo formato (YAML 1.2).
GitHub no hace distinción funcional entre ambas extensiones.

---

### 🧠 ¿Cuál conviene usar?

En la práctica:

* `.yml` → más común en repos públicos y ejemplos oficiales.
* `.yaml` → más explícito y semánticamente claro.

GitHub usa **`.yml` en la mayoría de su documentación oficial**, por ejemplo:

```bash
.github/workflows/main.yml
```

---

### 🎯 Recomendación práctica

Mantén consistencia en el repositorio.
Si ya tienes workflows `.yml`, sigue con `.yml`.

En proyectos profesionales suele verse:

```bash
server.yml
ci.yml
deploy.yml
release.yml
```
