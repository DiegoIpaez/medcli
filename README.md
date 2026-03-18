# MedCLI

MedCLI es una aplicación de línea de comandos para la gestión de una clínica médica. Permite administrar médicos, pacientes, turnos y generar reportes, todo desde la terminal.

## Tabla de Contenidos
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Comandos Útiles](#comandos-útiles)
- [Contribuir](#contribuir)
- [Licencia](#licencia)

## Requisitos
- Python 3.12 o superior
- [Poetry](https://python-poetry.org/) para la gestión de dependencias

## Instalación
1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/DiegoIpaez/medcli
   cd medcli
   ```
2. **Instala las dependencias y hooks de pre-commit:**
   ```bash
   make install
   ```
   Esto instalará todas las dependencias y configurará los hooks de pre-commit para asegurar la calidad del código.

## Uso
Para ejecutar la aplicación:
```bash
make run
```
Esto iniciará la interfaz de línea de comandos donde podrás navegar por los menús de médicos, pacientes, turnos y reportes.

## Estructura del Proyecto
```
medcli/
├── data/                # Archivos de migración y datos
├── src/                 # Código fuente principal
│   ├── database/        # Conexión, modelos y migraciones de la base de datos
│   ├── menus/           # Menús y lógica de negocio
│   │   ├── app/         # Menú principal y reportes
│   │   ├── medicos/     # Gestión de médicos
│   │   ├── pacientes/   # Gestión de pacientes
│   │   ├── turnos/      # Gestión de turnos
│   │   └── obras_sociales/ # Gestión de obras sociales
│   ├── ui/              # Utilidades de interfaz (colores, input, layout)
│   └── utils/           # Decoradores y utilidades generales
├── storage/reports/     # Reportes generados
├── Makefile             # Comandos de automatización
├── pyproject.toml       # Configuración de dependencias (Poetry)
└── .pre-commit-config.yaml # Configuración de pre-commit
```

## Comandos Útiles
- `make install`   : Instala dependencias y hooks de pre-commit
- `make run`       : Ejecuta la aplicación
- `make lint`      : Analiza el código con Ruff
- `make format`    : Formatea el código con Ruff
- `make fix`       : Corrige problemas automáticamente
- `make check`     : Ejecuta lint + format check
- `make hooks`     : Instala los hooks de pre-commit

## Arquitectura
- **Base de datos:** Utiliza SQLite y el ORM [Peewee](http://docs.peewee-orm.com/).
- **Menús:** Cada entidad (médicos, pacientes, turnos, obras sociales) tiene su propio menú y lógica de negocio en módulos separados.
- **UI:** Utilidades para mejorar la experiencia en la terminal (colores, mensajes, layouts).
- **Reportes:** Generación de reportes en PDF usando [ReportLab](https://www.reportlab.com/).
- **Pre-commit:** Se utiliza Ruff para linting y formateo automático del código.

## Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
