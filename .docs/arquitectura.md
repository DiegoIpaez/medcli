
# Arquitectura del Proyecto `medcli`
## Estructura de Carpetas y Archivos

```
medcli/
├── Makefile                # Comandos de automatización (tests, lint, etc.)
├── pyproject.toml          # Configuración y dependencias del proyecto Python
├── data/                   # Archivos de datos y base de datos
│   └── clinica.db          # Base de datos principal SQLite
├── src/                    # Código fuente principal
│   ├── __ini__.py
│   ├── main.py             # Punto de entrada de la aplicación
│   ├── database/           # Lógica de base de datos y modelos
│   │   ├── __ini__.py
│   │   ├── connection.py   # Conexión a la base de datos
│   │   ├── migration.py    # Migraciones de esquema
│   │   ├── models.py       # Definición de modelos de datos
│   │   ├── triggers.py     # Triggers y lógica asociada
│   ├── menus/              # Menús y lógica de navegación
│   │   ├── __init__.py
│   │   ├── app/            # Menú principal y vistas generales
│   │   │   ├── __init__.py
│   │   │   ├── app_menu.py
│   │   │   ├── app_reporte.py
│   │   │   ├── app_services.py
│   │   │   ├── app_vistas.py
│   │   ├── medicos/        # Menús y vistas para médicos
│   │   │   ├── __init__.py
│   │   │   ├── medicos_menu.py
│   │   │   ├── medicos_servicio.py
│   │   │   ├── medicos_vistas.py
│   │   ├── pacientes/      # Menús y vistas para pacientes
│   │   │   ├── __init__.py
│   │   │   ├── pacientes_menu.py
│   │   │   ├── pacientes_servicio.py
│   │   │   ├── pacientes_vistas.py
│   │   └── turnos/         # Menús y vistas para turnos
│   │       ├── turnos_menu.py
│   │       ├── turnos_service.py
│   │       ├── turnos_vistas.py
│   ├── ui/                 # Utilidades de interfaz de usuario
│   │   ├── __init__.py
│   │   ├── colores.py
│   │   ├── input.py
│   │   ├── layout.py
│   │   ├── mensajes.py
│   └── utils/              # Utilidades generales y helpers
│       ├── __init__.py
│       ├── cuil.py
│       ├── decorators.py
└── storage/                # Almacenamiento de archivos generados
     └── reports/            # Reportes exportados
```

### Descripción de Carpetas Principales

- **data/**: Archivos de datos persistentes, como la base de datos.
- **src/**: Todo el código fuente de la aplicación.
  - **database/**: Conexión, migraciones y modelos de la base de datos.
  - **menus/**: Lógica de menús y submenús por dominio (app, médicos, pacientes, turnos).
  - **ui/**: Utilidades para la interfaz de usuario (colores, layout, mensajes, input).
  - **utils/**: Funciones auxiliares y decoradores reutilizables.
- **storage/**: Archivos generados, como reportes exportados.

---

## ¿Cómo crear un nuevo módulo?

Para mantener la arquitectura modular, los nuevos módulos deben seguir la convención de las carpetas existentes en `src/menus/`.

### Pasos para agregar un nuevo módulo (ejemplo: "obras sociales")

1. **Crear la carpeta del módulo:**
    - Ubicación: `src/menus/obras_sociales/`
    - Archivos recomendados:
      - `__init__.py`
      - `obras_sociales_menu.py` (menú principal del módulo)
      - `obras_sociales_servicio.py` (lógica de negocio y acceso a datos)
      - `obras_sociales_vistas.py` (funciones de presentación/interfaz)

2. **Estructura sugerida de archivos:**
    - `*_menu.py`: Define el menú y las opciones disponibles para el usuario.
    - `*_servicio.py`: Implementa la lógica de negocio y operaciones sobre los datos.
    - `*_vistas.py`: Contiene funciones para mostrar información y recolectar input.

3. **Registrar el nuevo módulo:**
    - Importar y enlazar el menú principal del nuevo módulo en el menú general (`src/menus/app/app_menu.py`).

4. **Reutilizar utilidades:**
    - Usar funciones de `src/ui/` y `src/utils/` para mantener coherencia en la interfaz y lógica.

### Ejemplo de estructura para un nuevo módulo

```
src/menus/obras_sociales/
├── __init__.py
├── obras_sociales_menu.py
├── obras_sociales_servicio.py
└── obras_sociales_vistas.py
```

---

## Buenas prácticas

- Mantener la separación de responsabilidades: menú, lógica de negocio y vistas.
- Documentar cada función y archivo.
- Reutilizar componentes existentes.
- Seguir la convención de nombres para facilitar la navegación y el mantenimiento.

---

¿Dudas o sugerencias? ¡Contribuye a la documentación!
