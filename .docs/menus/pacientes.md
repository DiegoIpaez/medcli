# Módulo Pacientes — MedCLI

> Gestión integral de pacientes: registro, consulta, edición y eliminación, incluyendo validación de CUIT y asociación a obra social.

---

## Estructura de Archivos

| Archivo | Responsabilidad |
|---|---|
| `pacientes_menu.py` | Menú principal e interacción con el usuario |
| `pacientes_servicio.py` | Lógica de negocio y operaciones sobre los datos |
| `pacientes_vistas.py` | Presentación y visualización en pantalla |
| `__init__.py` | Inicialización del paquete |

---

## Menú Principal

```
--- Menú de Pacientes ---
1. Listar todos los pacientes
2. Buscar paciente
3. Registrar nuevo paciente
4. Editar paciente
5. Eliminar paciente
0. Volver al menú principal
```

---

## Datos mostrados en tabla

Todas las opciones de listado y búsqueda muestran los siguientes campos:

| Campo | Tipo |
|---|---|
| ID | Número |
| Nombre completo | Texto |
| CUIT | Texto |
| Fecha de nacimiento | Fecha (DD/MM/AAAA) |
| Obra Social | Texto (nombre) o "—" |

> **Mensaje de advertencia general:** Si no hay pacientes registrados, todas las opciones que requieren datos existentes muestran: _"No hay pacientes registrados."_ y regresan al menú.

---

## Flujo de cada opción

### 1 · Listar todos los pacientes

```
Usuario selecciona opción 1
    └─ ¿Hay pacientes registrados?
        ├─ SÍ → Muestra tabla completa con todos los pacientes
        └─ NO → Mensaje de advertencia → Regresa al menú
```

---

### 2 · Buscar paciente

```
Usuario selecciona opción 2
    └─ ¿Hay pacientes registrados?
        ├─ NO → Mensaje de advertencia → Regresa al menú
        └─ SÍ → Solicita término de búsqueda (nombre / CUIT)
                └─ ¿Hay coincidencias parciales?
                    ├─ SÍ → Muestra tabla con resultados encontrados
                    └─ NO → "No se encontraron resultados." → Regresa al menú
```

---

### 3 · Registrar nuevo paciente

**Datos solicitados:**

| Campo | Tipo | Validación |
|---|---|---|
| Nombre completo | Texto | No puede estar vacío |
| CUIT | Texto | No puede estar vacío · Debe ser válido (11 dígitos, verificador) · Único |
| Fecha de nacimiento | Fecha (DD/MM/AAAA) | Formato válido |
| Obra Social | Selección de lista | Puede ser "Sin obra social" o una opción válida |

```
Usuario selecciona opción 3
    └─ Ingresa nombre, CUIT, fecha de nacimiento y obra social
        └─ ¿Datos válidos y CUIT único?
            ├─ SÍ → Registra paciente → Mensaje de éxito
            └─ NO → Muestra error (CUIT inválido o duplicado, fecha inválida, etc.) → No registra
```

---

### 4 · Editar paciente

**Datos modificables** _(todos opcionales — dejar vacío conserva el valor actual)_:

| Campo | Tipo |
|---|---|
| Nombre completo | Texto |
| CUIT | Texto (valida formato y unicidad) |
| Fecha de nacimiento | Fecha (DD/MM/AAAA) |
| Obra Social | Selección de lista |

```
Usuario selecciona opción 4
    └─ ¿Hay pacientes registrados?
        ├─ NO → Mensaje de advertencia → Regresa al menú
        └─ SÍ → Muestra tabla completa → Solicita ID del paciente a editar
                └─ ¿ID válido y existente?
                    ├─ NO → Error de validación
                    └─ SÍ → Muestra datos actuales → Permite modificar campos
                            └─ Guarda cambios → Mensaje de confirmación con nombre actualizado
```

---

### 5 · Eliminar paciente

```
Usuario selecciona opción 5
    └─ ¿Hay pacientes registrados?
        ├─ NO → Mensaje de advertencia → Regresa al menú
        └─ SÍ → Muestra tabla completa → Solicita ID del paciente a eliminar
                └─ ¿ID válido y existente?
                    ├─ NO → Error de validación
                    └─ SÍ → Muestra advertencia con nombre y cantidad de turnos asociados → Solicita confirmación (sí/no)
                            ├─ CONFIRMA → Elimina paciente → Mensaje de éxito con nombre eliminado
                            └─ CANCELA → "Operación cancelada." → Regresa al menú
```

---

### 0 · Volver al menú principal

Regresa directamente al menú principal de la aplicación.
