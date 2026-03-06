# Módulo [Nombre del Módulo] — MedCLI

> [Breve descripción del módulo y su propósito principal en una línea.]

---

## Estructura de Archivos

| Archivo | Responsabilidad |
|---|---|
| `[modulo]_menu.py` | Menú principal e interacción con el usuario |
| `[modulo]_servicio.py` | Lógica de negocio y operaciones sobre los datos |
| `[modulo]_vistas.py` | Presentación y visualización en pantalla |
| `__init__.py` | Inicialización del paquete |

---

## Menú Principal

```
--- Menú de [Nombre del Módulo] ---
1. [Opción 1]
2. [Opción 2]
3. [Opción 3]
4. [Opción 4]
5. [Opción 5]
6. [Opción 6]
0. Volver al menú principal
```

---

## Datos mostrados en tabla

Todas las opciones de listado y búsqueda muestran los siguientes campos:

| Campo | Tipo |
|---|---|
| ID | Número |
| [Campo 2] | Texto |
| [Campo 3] | Texto |
| [Campo 4] | Texto |
| Estado | Activo / Inactivo |

> **Mensaje de advertencia general:** Si no hay registros, todas las opciones que requieren datos existentes muestran: _"No hay [entidades] registrados."_ y regresan al menú.

---

## Flujo de cada opción

### 1 · [Nombre opción 1]

```
Usuario selecciona opción 1
    └─ ¿Hay registros?
        ├─ SÍ → Muestra tabla completa
        └─ NO → Mensaje de advertencia → Regresa al menú
```

---

### 2 · [Nombre opción 2]

```
Usuario selecciona opción 2
    └─ ¿Hay registros activos?
        ├─ SÍ → Muestra tabla filtrada (solo activos)
        └─ NO → Mensaje de advertencia → Regresa al menú
```

---

### 3 · [Nombre opción 3 — Búsqueda]

```
Usuario selecciona opción 3
    └─ ¿Hay registros?
        ├─ NO → Mensaje de advertencia → Regresa al menú
        └─ SÍ → Solicita término de búsqueda ([campo1] / [campo2] / [campo3])
                └─ ¿Hay coincidencias parciales?
                    ├─ SÍ → Muestra tabla con resultados encontrados
                    └─ NO → "No se encontraron resultados." → Regresa al menú
```

---

### 4 · [Nombre opción 4 — Registro]

**Datos solicitados:**

| Campo | Tipo | Validación |
|---|---|---|
| [Campo 1] | Texto | No puede estar vacío |
| [Campo 2] | Texto | No puede estar vacío · Debe ser único |
| [Campo 3] | Selección de lista | Debe ser una opción válida |

```
Usuario selecciona opción 4
    └─ Ingresa [campo1], [campo2] y [campo3]
        └─ ¿Datos válidos y [campo único] no duplicado?
            ├─ SÍ → Registra → Mensaje de éxito
            └─ NO → Muestra error → No registra
```

---

### 5 · [Nombre opción 5 — Edición]

**Datos modificables** _(todos opcionales — dejar vacío conserva el valor actual)_:

| Campo | Tipo |
|---|---|
| [Campo 1] | Texto |
| [Campo 2] | Texto |
| [Campo 3] | Selección de lista |
| Estado activo | s / n |

```
Usuario selecciona opción 5
    └─ ¿Hay registros?
        ├─ NO → Mensaje de advertencia → Regresa al menú
        └─ SÍ → Muestra tabla completa → Solicita ID a editar
                └─ ¿ID válido y existente?
                    ├─ NO → Error de validación
                    └─ SÍ → Muestra datos actuales → Permite modificar campos
                            └─ Guarda cambios → Mensaje de confirmación
```

---

### 6 · [Nombre opción 6 — Eliminación]

```
Usuario selecciona opción 6
    └─ ¿Hay registros?
        ├─ NO → Mensaje de advertencia → Regresa al menú
        └─ SÍ → Muestra tabla completa → Solicita ID a eliminar
                └─ ¿ID válido y existente?
                    ├─ NO → Error de validación
                    └─ SÍ → Muestra advertencia con nombre → Solicita confirmación (sí/no)
                            ├─ CONFIRMA → Elimina → Mensaje de éxito
                            └─ CANCELA → "Operación cancelada." → Regresa al menú
```

---

### 0 · Volver al menú principal

Regresa directamente al menú principal de la aplicación.