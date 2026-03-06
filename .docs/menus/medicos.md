# Módulo Médicos — MedCLI

> Gestión integral de profesionales médicos: registro, consulta, modificación y eliminación.

---

## Estructura de Archivos

| Archivo | Responsabilidad |
|---|---|
| `medicos_menu.py` | Menú principal e interacción con el usuario |
| `medicos_servicio.py` | Lógica de negocio y operaciones sobre los datos |
| `medicos_vistas.py` | Presentación y visualización en pantalla |
| `__init__.py` | Inicialización del paquete |

---

## Menú Principal

```
--- Menú de Médicos ---
1. Listar todos los médicos
2. Listar médicos activos
3. Buscar médico
4. Registrar nuevo médico
5. Editar médico
6. Eliminar médico
0. Volver al menú principal
```

---

## Datos mostrados en tabla

Todas las opciones de listado y búsqueda muestran los siguientes campos:

| Campo | Tipo |
|---|---|
| ID | Número |
| Nombre completo | Texto |
| Especialidad | Texto |
| Matrícula | Texto |
| Estado | Activo / Inactivo |

> **Mensaje de advertencia general:** Si no hay médicos registrados, todas las opciones que requieren datos existentes muestran: _"No hay médicos registrados."_ y regresan al menú.

---

## Flujo de cada opción

### 1 · Listar todos los médicos

```
Usuario selecciona opción 1
    └─ ¿Hay médicos registrados?
        ├─ SÍ → Muestra tabla completa con todos los médicos
        └─ NO → Mensaje de advertencia → Regresa al menú
```

---

### 2 · Listar médicos activos

```
Usuario selecciona opción 2
    └─ ¿Hay médicos activos?
        ├─ SÍ → Muestra tabla filtrada (solo activos)
        └─ NO → Mensaje de advertencia → Regresa al menú
```

---

### 3 · Buscar médico

```
Usuario selecciona opción 3
    └─ ¿Hay médicos registrados?
        ├─ NO → Mensaje de advertencia → Regresa al menú
        └─ SÍ → Solicita término de búsqueda (nombre / especialidad / matrícula)
                └─ ¿Hay coincidencias parciales?
                    ├─ SÍ → Muestra tabla con resultados encontrados
                    └─ NO → "No se encontraron resultados." → Regresa al menú
```

---

### 4 · Registrar nuevo médico

**Datos solicitados:**

| Campo | Tipo | Validación |
|---|---|---|
| Nombre completo | Texto | No puede estar vacío |
| Matrícula | Texto | No puede estar vacío · Debe ser única en el sistema |
| Especialidad | Selección de lista | Debe ser una opción válida |

```
Usuario selecciona opción 4
    └─ Ingresa nombre, matrícula y especialidad
        └─ ¿Datos válidos y matrícula única?
            ├─ SÍ → Registra médico → Mensaje de éxito
            └─ NO → Muestra error (matrícula duplicada u otro) → No registra
```

---

### 5 · Editar médico

**Datos modificables** _(todos opcionales — dejar vacío conserva el valor actual)_:

| Campo | Tipo |
|---|---|
| Nombre completo | Texto |
| Matrícula | Texto |
| Especialidad | Selección de lista |
| Estado activo | s / n |

```
Usuario selecciona opción 5
    └─ ¿Hay médicos registrados?
        ├─ NO → Mensaje de advertencia → Regresa al menú
        └─ SÍ → Muestra tabla completa → Solicita ID del médico a editar
                └─ ¿ID válido y existente?
                    ├─ NO → Error de validación
                    └─ SÍ → Muestra datos actuales → Permite modificar campos
                            └─ Guarda cambios → Mensaje de confirmación con nombre actualizado
```

---

### 6 · Eliminar médico

```
Usuario selecciona opción 6
    └─ ¿Hay médicos registrados?
        ├─ NO → Mensaje de advertencia → Regresa al menú
        └─ SÍ → Muestra tabla completa → Solicita ID del médico a eliminar
                └─ ¿ID válido y existente?
                    ├─ NO → Error de validación
                    └─ SÍ → Muestra advertencia con nombre del médico → Solicita confirmación (sí/no)
                            ├─ CONFIRMA → Elimina médico → Mensaje de éxito con nombre eliminado
                            └─ CANCELA → "Operación cancelada." → Regresa al menú
```

---

### 0 · Volver al menú principal

Regresa directamente al menú principal de la aplicación.