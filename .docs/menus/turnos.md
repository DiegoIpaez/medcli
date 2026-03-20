# Módulo Turnos — MedCLI

> Gestión y administración de turnos médicos: alta, consulta, cambio de estado y registro de duración real.

---

## Estructura de Archivos

| Archivo | Responsabilidad |
|---|---|
| `turnos_menu.py` | Menú principal e interacción con el usuario |
| `turnos_service.py` | Lógica de negocio y operaciones sobre los datos |
| `turnos_vistas.py` | Presentación y visualización en pantalla |
| `__init__.py` | Inicialización del paquete |

---

## Menú Principal

```
--- Menú de Turnos ---
1. Crear nuevo turno
2. Ver agenda diaria por médico
3. Cambiar estado de un turno
4. Registrar duración real de consulta
5. Ver turnos de un paciente
0. Volver al menú principal
```

---

## Datos mostrados en tabla

Las opciones de listado y búsqueda muestran los siguientes campos (según contexto):

| Campo | Tipo |
|---|---|
| ID | Número |
| Fecha | Fecha (DD/MM/AAAA) |
| Hora | Hora (HH:MM) |
| Médico | Texto |
| Especialidad | Texto |
| Paciente | Texto |
| CUIL Paciente | Texto |
| Estado | Reservado / Atendido / Cancelado / Ausente |
| Duración | Minutos (estimada o real) |
| ET | Entre-turno (marcado) |
| Notas | Texto |

> **Mensaje de advertencia general:** Si no hay turnos registrados, todas las opciones que requieren datos existentes muestran: _"No hay turnos registrados."_ y regresan al menú.

---

## Flujo de cada opción

### 1 · Crear nuevo turno

**Datos solicitados:**

| Campo | Tipo | Validación |
|---|---|---|
| Paciente | Selección de lista (búsqueda por nombre/CUIL) | Debe existir |
| Médico | Selección de lista (solo activos) | Debe existir |
| Fecha | Fecha (DD/MM/AAAA) | Formato válido |
| Horario | Hora (HH:MM) | Formato válido · Sin conflicto (o entre-turno con confirmación) |
| Notas | Texto (opcional) | — |

```
Usuario selecciona opción 1
    └─ Busca y selecciona paciente
        └─ Busca y selecciona médico
            └─ Ingresa fecha y horario
                └─ ¿Conflicto de horario?
                    ├─ NO → Ingresa notas → Registra turno → Mensaje de éxito
                    └─ SÍ → Advierte conflicto → ¿Confirma entre-turno?
                            ├─ SÍ → Registra como entre-turno → Mensaje de éxito
                            └─ NO → Cancela operación
```

---

### 2 · Ver agenda diaria por médico

```
Usuario selecciona opción 2
    └─ Selecciona médico activo
        └─ Ingresa fecha
            └─ ¿Hay turnos para ese médico y fecha?
                ├─ SÍ → Muestra tabla con: Hora, Paciente, CUIL, Estado, Duración, ET, Notas
                └─ NO → Mensaje de advertencia → Regresa al menú
```

---

### 3 · Cambiar estado de un turno

**Datos solicitados:**

| Campo | Tipo | Validación |
|---|---|---|
| ID del turno | Número | Debe existir |
| Nuevo estado | Selección de lista | Debe ser válido |

```
Usuario selecciona opción 3
    └─ Ingresa ID del turno
        └─ ¿ID válido y existente?
            ├─ NO → Error de validación
            └─ SÍ → Muestra datos actuales → Selecciona nuevo estado
                    └─ Actualiza estado → Mensaje de confirmación
```

---

### 4 · Registrar duración real de consulta

**Datos solicitados:**

| Campo | Tipo | Validación |
|---|---|---|
| ID del turno | Número | Debe existir y estar pendiente |
| Duración real | Número (minutos) | Entero positivo |

```
Usuario selecciona opción 4
    └─ ¿Hay turnos pendientes?
        ├─ NO → Mensaje de advertencia → Regresa al menú
        └─ SÍ → Muestra tabla de turnos pendientes → Ingresa ID
                └─ ¿ID válido y existente?
                    ├─ NO → Error de validación
                    └─ SÍ → Ingresa duración real
                            └─ Actualiza duración y estado → Mensaje de éxito
```

---

### 5 · Ver turnos de un paciente

```
Usuario selecciona opción 5
    └─ Busca y selecciona paciente
        └─ ¿El paciente tiene turnos?
            ├─ SÍ → Muestra tabla con: ID, Fecha, Hora, Médico, Especialidad, Estado, Duración
            └─ NO → Mensaje de advertencia → Regresa al menú
```

---

### 0 · Volver al menú principal

Regresa directamente al menú principal de la aplicación.
