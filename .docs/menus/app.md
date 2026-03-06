# Módulo Menú Principal — MedCLI

> Punto de entrada y navegación central del sistema: acceso a gestión de pacientes, médicos, turnos y generación de reportes.

---

## Estructura de Archivos

| Archivo | Responsabilidad |
|---|---|
| `app_menu.py` | Menú principal e interacción con el usuario |
| `app_services.py` | Lógica de negocio para reportes y métricas globales |
| `app_vistas.py` | Presentación, generación y visualización de reportes |
| `__init__.py` | Inicialización del paquete |

---

## Menú Principal

```
--- MENÚ PRINCIPAL ---
1. Gestión de Pacientes
2. Gestión de Médicos
3. Gestión de Turnos
4. Generar Reporte
0. Salir
```

---


## Funcionalidades principales

- **Gestión de Pacientes:** Acceso al módulo de pacientes para registrar, consultar, editar y eliminar pacientes.
- **Gestión de Médicos:** Acceso al módulo de médicos para registrar, consultar, editar y eliminar médicos.
- **Gestión de Turnos:** Acceso al módulo de turnos para crear, consultar, modificar y eliminar turnos médicos.
- **Generar Reporte:** Genera un reporte PDF con indicadores y métricas globales del sistema, incluyendo:
    - **Indicadores generales:**
        - Total de turnos (no cancelados)
        - Cantidad y tasa de ausentismo
    - **Médico con mayor cantidad de turnos atendidos:**
        - Nombre, especialidad y cantidad
    - **Turnos por mes:**
        - Tabla con cantidad de turnos agrupados por mes y año
    - **Promedio de duración de consultas por médico:**
        - Tabla con médico, cantidad de consultas y promedio en minutos
    - **Resumen por médico:**
        - Tabla con médico, especialidad, total de turnos, atendidos, ausentes y cancelados
    - El reporte se guarda en la carpeta `storage/reports/` y se abre automáticamente tras su generación.
- **Salir:** Finaliza la aplicación mostrando un mensaje de despedida.

---

## Flujo de cada opción

### 1 · Gestión de Pacientes

```
Usuario selecciona opción 1
    └─ Accede al menú de Pacientes (ver documentación de ese módulo)
```

---

### 2 · Gestión de Médicos

```
Usuario selecciona opción 2
    └─ Accede al menú de Médicos (ver documentación de ese módulo)
```

---

### 3 · Gestión de Turnos

```
Usuario selecciona opción 3
    └─ Accede al menú de Turnos (ver documentación de ese módulo)
```

---

### 4 · Generar Reporte

```
Usuario selecciona opción 4
    └─ El sistema genera un reporte PDF con:
        - Tasa de ausentismo
        - Promedio de duración de consulta por médico
        - Médico con más turnos atendidos
        - Cantidad de turnos por mes
        - Estadísticas de médicos
    └─ Muestra mensaje de éxito y abre el PDF generado
```

---

### 0 · Salir

```
Usuario selecciona opción 0
    └─ El sistema muestra mensaje de despedida y finaliza la aplicación
```

---

> **Nota:** Todas las opciones inválidas muestran un mensaje de error y permiten reintentar.
