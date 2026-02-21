En GitHub Actions, **esa vista que estás viendo (panel izquierdo de “All workflows”) no muestra el `name:` del workflow**, sino **el nombre del archivo `.yml` dentro de `.github/workflows/`**.

### ✔ Por qué aparece así:

* Cuando **tu archivo SÍ tiene `name:` definido**, GitHub muestra ese nombre **solo dentro del workflow** cuando lo abres.
* Pero en la **lista de workflows**, GitHub siempre usa el **nombre del archivo** como etiqueta principal.
* Por eso tú ves:

```
.github/workflows/postgres-env-vars…
```

…porque **ese es el nombre del archivo** a pesar de que dentro tengas algo como:

```yaml
name: PostgreSQL Integration Test (Workflow Environment Variables)
```

### ✔ Cómo hacer que se vea más bonito

Si quieres que en la lista aparezca un nombre “bueno”, cambia el nombre del archivo, por ejemplo:

| Archivo                                      | Cómo se verá         |
| -------------------------------------------- | -------------------- |
| `.github/workflows/postgres-env-vars.yml`    | postgres-env-vars    |
| `.github/workflows/postgres-integration.yml` | postgres-integration |
| `.github/workflows/pg-env.yml`               | pg-env               |

GitHub **no usa el `name:` para renombrar el archivo**.

### ✔ Lo que puedes hacer

Renombra el archivo a algo más claro:

```
.github/workflows/postgres-env.yml
```

En Linux:

```bash
mv .github/workflows/postgres-env-vars.yml .github/workflows/postgres-env.yml
```

### 🧩 Resumen

* **GitHub muestra el nombre del archivo, NO el `name:` del workflow.**
* El `name:` solo aparece cuando abres el workflow.
* Si quieres un nombre diferente en el listado → **renombra el archivo `.yml`**.

---

Si querés te recomiendo un buen nombre estándar para tu workflow según lo que hace. ¿Cómo quieres llamarlo?
