import sqlite3
from .models import ObraSocial, Paciente, Medico, Turno
from .triggers import crear_timestamp_triggers, crear_turnos_triggers


DB_PATH = "data/clinica.db"
TIMESTAMP_TABLES = ["obras_sociales", "pacientes", "medicos", "turnos"]


def db_exists():
    """Verifica si la DB ya existe y tiene tablas"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name IN (?, ?, ?, ?)",
            TIMESTAMP_TABLES,
        )
        tables_exist = len(cursor.fetchall()) > 0
        conn.close()
        return tables_exist
    except sqlite3.OperationalError:
        return False


def needs_triggers():
    """Verifica si faltan triggers críticos"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'trg_%'"
        )
        existing_triggers = {row[0] for row in cursor.fetchall()}
        conn.close()

        required_triggers = {
            f"trg_{table}_created_at" for table in TIMESTAMP_TABLES
        } | {
            "trg_turnos_duracion_entre_turno",
            "trg_turnos_conflicto_medico_insert",
            "trg_turnos_conflicto_paciente_insert",
        }

        return not required_triggers.issubset(existing_triggers)
    except:
        return True


def migrate(db):
    if not db_exists():
        print("🆕 Creando base de datos por primera vez...")

        db.create_tables([ObraSocial, Paciente, Medico, Turno], safe=True)
        crear_timestamp_triggers(TIMESTAMP_TABLES)
        crear_turnos_triggers()

        print("✅ Base de datos creada con triggers!")
    elif needs_triggers():
        print("🔧 Actualizando triggers faltantes...")

        crear_timestamp_triggers(TIMESTAMP_TABLES)
        crear_turnos_triggers()

        print("✅ Triggers actualizados!")
    else:
        print("✅ Base de datos y triggers ya están OK!")
