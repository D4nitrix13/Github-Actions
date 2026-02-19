Perfecto — si lo quieres **multidirectorio (global en todo el proyecto, sin importar profundidad)**, estas reglas ya aplican recursivamente en Git:

```gitignore
# Ignorar todos los __pycache__ en cualquier subdirectorio
__pycache__/

# Ignorar todos los archivos compilados de Python en cualquier nivel
*.py[cod]

# Ignorar archivo de coverage en la raíz o subdirectorios
.coverage
.coverage.*
```

---

## 🔎 Por qué esto ya es multidirectorio

En `.gitignore`:

* `__pycache__/` → ignora cualquier carpeta llamada `__pycache__` en cualquier nivel.
* `*.py[cod]` → ignora `*.pyc`, `*.pyo`, `*.pyd` en cualquier nivel.
* `.coverage` → ignora el archivo donde aparezca (normalmente raíz).
* `.coverage.*` → ignora archivos combinados como `.coverage.machine1`.

---

## 🎯 Si quieres hacerlo explícitamente “global”

Podrías usar:

```gitignore
**/__pycache__/
**/*.py[cod]
**/.coverage
**/.coverage.*
```

Pero realmente **no es necesario**, porque Git ya interpreta las reglas sin `/` inicial como recursivas.

---

## 🧠 Resumen técnico

| Regla          | ¿Es recursiva? |
| -------------- | -------------- |
| `__pycache__/` | ✅ Sí           |
| `*.pyc`        | ✅ Sí           |
| `.coverage`    | ✅ Sí           |

---

Si quieres, puedo explicarte la diferencia entre:

* `foo/`
* `/foo/`
* `**/foo/`

Y cómo funciona el pattern matching interno de Git (muy útil cuando el repo crece).
